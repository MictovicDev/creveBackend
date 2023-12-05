from django.shortcuts import render
from rest_framework import generics,permissions, response, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.response import Response
from core.models import *

# Create your views here.



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

        
class CreativeView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(role='Creative')

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save(role='Creative')
            proflie = Profile.objects.create(user=user)
            token = str(RefreshToken.for_user(user))
            user.token = token
            user.is_active = True
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(role='Creative')

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save(role='User')
            proflie = Profile.objects.create(user=user)
            token = str(RefreshToken.for_user(user))
            user.token = token
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)