from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ProfileSerializer, RegisterSerializer

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
    
@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"detail": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)