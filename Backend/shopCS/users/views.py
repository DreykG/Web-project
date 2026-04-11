from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated] 

    def list(self, request):
        user = request.user
    
        profile, created = Profile.objects.get_or_create(user=user)
        
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)