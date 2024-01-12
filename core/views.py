from django.shortcuts import render, redirect
from rest_framework import generics,permissions, response, status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView
from core.models import *
from . import email
from . import urls
from core.serializers import *

# Create your views here.

print("hello")

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

        
class ClientView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(role='Client')

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save(role='Client')
            proflie = ClientProfile.objects.create(user=user)
            token = str(RefreshToken.for_user(user))
            user.token = token
            fullname = user.fullname
            useremail = user.email
            user.is_active = True
            user.save()
            email.send_linkmail(fullname,useremail,token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TalentView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(role='Talent')

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save(role='Talent')
            proflie = TalentProfile.objects.create(user=user)
            token = str(RefreshToken.for_user(user))
            user.token = token
            fullname = user.fullname
            useremail = user.email
            user.is_active = True
            user.save()
            email.send_linkmail(fullname,useremail,token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccount(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request,token):
        try:
            user = User.objects.get(token=token)
            print(user)
            user.is_active = True
            user.save()
            data = {
                'user': user.email,
                'token': user.token
            }
            if user.role == 'Client':
                return redirect('https://creve.vercel.app/login')
            return redirect('https://creve.vercel.app/loginCreative')
        except:
            data = {'message': "User does not exist"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)


class ClientUpdateView(generics.RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = User.objects.all()
    serializer_class = UpdateClientSerializer
    permission_classes = [permissions.AllowAny]


    def get_object(self):
        user = self.request.user
        user = User.objects.get(email=user)
        print(user)
        return user
    
    # def update(self, request,*args, **kwargs):
    #     profile = self.get_object()
    #     serializer = self.get_serializer(profile, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


   

    # def get_object(self):
    #     pk = self.request.user.id
    #     try:
    #         user = User.objects.get(id=pk)
    #     except:
    #          return Response({"error_message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
    #     profile = ClientProfile.objects.get_or_create(user=user)[0]
    #     return profile

    
        
class TalentUpdateView(generics.RetrieveUpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = User.objects.all()
    serializer_class = TalentProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_object(self):
        pk = self.request.user.id
        try:
            user = User.objects.get(id=pk)
        except:
             return Response({"error_message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        profile = ClientProfile.objects.get_or_create(user=user)[0]
        return profile

    def update(self, request,*args, **kwargs):
        profile = self.get_object()
        print(profile)
        serializer = self.get_serializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentApi(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        data = {}
        for item in urls.urlpatterns:
            name = ' '.join(item.name.split('_'))
            data[name.capitalize()] = str(item.pattern)
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
