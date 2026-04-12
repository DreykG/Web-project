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
        user = request.user
        
        try:
            current_member = GangMember.objects.get(gang=gang, user=user)
            if current_member.role < 2: 
                return Response({"detail": "Only Admins or Owners can accept requests."}, status=403)
        except GangMember.DoesNotExist:
            return Response({"detail": "You are not a member of this gang."}, status=403)

        try:
            join_request = GangJoinRequest.objects.get(id=request_id, gang=gang, status='pending')
        except GangJoinRequest.DoesNotExist:
            return Response({"detail": "Request not found or already processed."}, status=404)

        if gang.members.count() >= 15:
            return Response({"detail": "Gang is full (max 15 members)."}, status=400)

        with transaction.atomic():

            GangMember.objects.create(gang=gang, user=join_request.user, role=1) # Роль 1 - User
            

            join_request.status = 'accepted'
            join_request.save()
            

            gang.update_status()

        return Response({"detail": f"User {join_request.user.username} has been accepted to the gang!"})
