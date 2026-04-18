from datetime import timezone

from django.shortcuts import render


from decimal import Decimal
from rest_framework.decorators import api_view, permission_classes, action
# from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status,viewsets
from .models import Gang, GangJoinRequest, GangMember, GangMessage, GangVaultRental
from shop.models import InventoryItem
from .serializers import (
    GangSerializer, 
    GangMessageSerializer, 
    GangJoinRequestSerializer, 
    GangMemberSerializer
    )
from django.db import transaction


class GangViewSet(viewsets.ModelViewSet):
    queryset = Gang.objects.all()
    serializer_class = GangSerializer

    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        user = self.request.user

        if GangMember.objects.filter(user=user).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError("You are already a member of a gang.")
        
        with transaction.atomic():
            gang = serializer.save(owner=user)
            GangMember.objects.create(gang=gang, user=user, role=3)
        return Response({"detail" : "The gang created"})
    
    @action(detail=True, methods=['get'])
    def members(self,request, pk=None):
        gang = self.get_object()
        queryset = GangMember.objects.filter(gang=gang).select_related('user').order_by('-role')
        serializer = GangMemberSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
        gang = self.get_object()
        user = request.user

        if GangMember.objects.filter(user=user).exists():
            return Response({"detail": "You are already in a gang."}, status=400)
        
        if not gang.is_open:
            return Response({"detail": "This gang is full or closed."}, status=400)

        request_obj, created = GangJoinRequest.objects.get_or_create(gang=gang, user=user)
        if not created:
            return Response({"detail": "Application already sent."}, status=400)
        
        return Response({"detail": "Application sent!"})


    @action(detail=True, methods=['post'], url_path='accept-request/(?P<request_id>[^/.]+)')
    def accept_request(self, request, pk=None, request_id=None):
        gang = self.get_object()
        
        current_member = GangMember.objects.get(gang=gang, user=request.user)
        if current_member.role < 2:
            return Response({"detail": "No permission."}, status=403)

        try:
            join_request = GangJoinRequest.objects.get(id=request_id, gang=gang, status='pending')
        except GangJoinRequest.DoesNotExist:
            return Response({"detail": "Request not found."}, status=404)

        if gang.members.count() >= 15:
            return Response({"detail": "Gang is full."}, status=400)

        with transaction.atomic():
            target_user = join_request.user
            GangMember.objects.create(gang=gang, user=target_user, role=1)
            

            GangJoinRequest.objects.filter(user=target_user).delete()
            gang.update_status()

        return Response({"detail": f"User {target_user.username} accepted and other requests cleared."})
    
    
    @action(detail=True, methods=(['get']))
    def show_requests(self, request, pk=None):
        gang = self.get_object()

        try:
            current_member = GangMember.objects.get(gang=gang, user=request.user)
            if current_member.role < 2: # 1-User, 2-Admin, 3-Owner
                return Response({"detail": "No permission (Admins/Owners only)."}, status=403)
        except GangMember.DoesNotExist:
            return Response({"detail": "You are not a member of this gang."}, status=403)
        

        queryset = GangJoinRequest.objects.filter(
            gang=gang,
            status='pending'
        )
        serializer = GangJoinRequestSerializer(queryset, many=True)
        return Response(serializer.data)


    @action(detail=True, methods=['get'])
    def vault(self, request, pk=None):
        gang = self.get_object()
        
        if not gang.members.filter(user=request.user).exists():
            return Response({"detail": "You are not a member of this gang."}, status=403)
        items = gang.vault_items.filter(status='in_gang')
        from shop.serializers import InventoryItemSerializer
        serializer = InventoryItemSerializer(items, many=True)
        
        return Response(serializer.data)


    @action(detail=True, methods=['post'], url_path='deposit_item/(?P<item_id>[^/.]+)')
    def deposit_item(self, request, pk=None, item_id=None):
        gang = self.get_object()
        user = request.user

        try:
            item = InventoryItem.objects.get(id=item_id, user=user, status='in_inventory')
        except InventoryItem.DoesNotExist:
            return Response({"detail": "Item not found."}, status=404)

        with transaction.atomic():
            item.user = None 
            item.status = 'in_gang'
            item.gang = gang

            item.save()

        return Response({"detail": f"{item.skin.name} added to vault. Pledge value: ${item.price}"})
    


    @action(detail=True, methods=['post'], url_path='rent/(?P<item_id>[^/.]+)')
    def rent_item(self, request, pk=None, item_id=None):
        gang = self.get_object()
        user = request.user

        try:
            item = InventoryItem.objects.get(id=item_id, gang=gang, status='in_gang')
        except InventoryItem.DoesNotExist:
            return Response({"detail": "Item not available."}, status=404)
 
        
        pledge_amount = item.price 

        if user.balance < pledge_amount:
            return Response({"detail": f"Need ${pledge_amount} for deposit. Your balance: ${user.balance}"}, status=400)

        with transaction.atomic():

            user.balance -= pledge_amount
            user.save()

            rental = GangVaultRental.objects.create(
                gang=gang,
                user=user,
                item=item,
                deposit_amount=pledge_amount,
                status='active'
            )

            item.status = 'rented_from_gang'
            item.user = user
            item.save()

        return Response({"detail": f"Item rented. ${pledge_amount} frozen as deposit."})
    


    @action(detail=True, methods=['post'], url_path='return_item/(?P<item_id>[^/.]+)')
    def return_item(self, request, pk=None, item_id=None):
        user = request.user
        
        try:
            rental = GangVaultRental.objects.get(
                item_id=item_id,
                user=user, 
                status='active'
            )
        except GangVaultRental.DoesNotExist:
            return Response({"detail": "Active rental record not found."}, status=404)

        with transaction.atomic():

            deposit = rental.deposit_amount
            fee = deposit * Decimal('0.03')
            refund = deposit - fee

            
            user.balance += refund
            user.save()

            gang = rental.gang
            gang.treasury += fee
            gang.save()

            item = rental.item
            item.status = 'in_gang'
            item.user = None
            item.save()

            rental.delete()

            GangMessage.objects.create(
                gang=gang,
                user=user,
                text=f"Returned {item.skin.name} to vault. Fee ${fee} paid to treasury."
            )

            

        return Response({
            "detail": "Item returned successfully!",
            "refunded_amount": refund,
            "fee_taken": fee
        })
    
    @action(detail=True, methods=['post'], url_path='promote/(?P<target_user_id>[^/.]+)')
    def promote(self, request, pk=None, target_user_id=None):
        gang = self.get_object()
        current_user = request.user

        try:
            boss = GangMember.objects.get(gang=gang, user=current_user, role=3)
        except GangMember.DoesNotExist:
            return Response({"detail": "Only the Owner can promote members."}, status=403)
        
        try:
            target_member = GangMember.objects.get(gang=gang, user_id=target_user_id)
        except GangMember.DoesNotExist:
            return Response({"detail": "Target user not found in this gang."}, status=404)
        
        with transaction.atomic():
            if target_member.role == 1:
                target_member.role = 2
                target_member.save()
                message = f"{target_member.user.username} promoted to Admin."

            elif target_member.role == 2:
                target_member.role = 3
                target_member.save()
                message = f"{target_member.user.username} promoted to Owner."

                boss.role = 2
                boss.save()

                gang.owner = target_member.user
                gang.save()
                message = f"Power transferred! {target_member.user.username} is the new Owner."
            else:
                return Response({"detail": "Cannot promote further."}, status=400)
        return Response({"detail": message})
    

    @action(detail=True, methods=['post'], url_path='demote/(?P<target_user_id>[^/.]+)')
    def demote(self, request, pk=None, target_user_id=None):
        gang = self.get_object()
        current_user = request.user

        if not GangMember.objects.filter(gang=gang, user=request.user, role=3).exists():
            return Response({"detail": "Only the Owner can demote members."}, status=403)

        try:
            target_member = GangMember.objects.get(gang=gang, user_id=target_user_id)
        except GangMember.DoesNotExist:
            return Response({"detail": "Target user not found."}, status=404)
        
        if target_member.role == 2:
            target_member.role = 1
            target_member.save()
            return Response({"detail": f"{target_member.user.username} demoted to Member."})

        return Response({"detail": "Cannot demote further (user is already at lowest rank)."}, status=400)
    
    @action(detail=True, methods=['post'], url_path='kick/(?P<target_user_id>[^/.]+)')
    def kick(self, request, pk=None, target_user_id=None):
        gang = self.get_object()
        current_user = request.user

        try:
            initiator = GangMember.objects.get(gang=gang, user=current_user)
            if initiator.role < 2:
                return Response({"detail": "Only Admins and Owners can kick members."}, status=403)
        except GangMember.DoesNotExist:
            return Response({"detail": "You are not a member of this gang."}, status=403)

        try:
            target_member = GangMember.objects.get(gang=gang, user_id=target_user_id)
        except GangMember.DoesNotExist:
            return Response({"detail": "Target user not found in this gang."}, status=404)

        if initiator.role <= target_member.role:
            return Response({"detail": "You cannot kick someone with a higher or equal rank."}, status=403)

        with transaction.atomic():

            active_rentals = GangVaultRental.objects.filter(
                user_id=target_user_id, 
                gang=gang, 
                status='active'
            )

            total_confiscated = 0
            for rental in active_rentals:

                total_confiscated += rental.deposit_amount
                
                rental.delete()

            gang.treasury += total_confiscated
            gang.save()

            target_member.delete()
            gang.update_status()

        message = f"User kicked. "
        if total_confiscated > 0:
            message += f"${total_confiscated} in deposits was confiscated to the treasury."
        
        return Response({"detail": message})
    

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        gang = self.get_object()
        user = request.user

        try:
            member = GangMember.objects.get(gang=gang, user=user)
        except GangMember.DoesNotExist:
            return Response({"detail": "You are not a member of this gang."}, status=404)

        if member.role == 3:
            other_members = GangMember.objects.filter(gang=gang).exclude(user=user)
            if other_members.exists():
                return Response({
                    "detail": "As the Owner, you must promote someone else to Owner before leaving, or use 'disband' to delete the gang."
                }, status=400)
            else:

                with transaction.atomic():
                    member.delete()
                    gang.delete()
                return Response({"detail": "You were the last member. Gang disbanded."})

        
        with transaction.atomic():

            active_rentals = GangVaultRental.objects.filter(
                user=user, 
                gang=gang, 
                status='active'
            )

            total_confiscated = 0
            for rental in active_rentals:
                total_confiscated += rental.deposit_amount
                
                item = rental.item
                item.status = 'owned' 
                item.user = user
                item.save()

                rental.delete()

            if total_confiscated > 0:
                gang.treasury += total_confiscated
                gang.save()

            member.delete()
            gang.update_status()

        res_msg = "You have left the gang."
        if total_confiscated > 0:
            res_msg += f" Your deposits (${total_confiscated}) were donated to the gang treasury as you kept the items."
            
        return Response({"detail": res_msg})
    

    @action(detail=True, methods=['post'], url_path='send_message')
    def send_message(self, request, pk=None):
        gang = self.get_object()
        
        if not gang.members.filter(user=request.user).exists():
            return Response({"detail": "You are not a member of this gang."}, status=403)

        text = request.data.get('text')
        if not text:
            return Response({"detail": "Message cannot be empty."}, status=400)

        message = GangMessage.objects.create(
            gang=gang,
            user=request.user,
            text=text
        )

        return Response({"message": str(message)})

    @action(detail=True, methods=['get'], url_path='chat_history')
    def chat_history(self, request, pk=None):
        gang = self.get_object()
        
        if not gang.members.filter(user=request.user).exists():
            return Response({"detail": "Access denied."}, status=403)


        messages = gang.messages.all().order_by('created_at')[:20]
        

        from .serializers import GangMessageSerializer 
        serializer = GangMessageSerializer(messages, many=True)
        
        return Response(serializer.data)