from django.shortcuts import render, redirect
from rest_framework import generics,permissions, response, status
from rest_framework.decorators import api_view
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
import requests
from . import urls
from core.serializers import *
from .models import TalentProfile
# Create your views here.



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


class ClientUpdateGetDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role='Client')
    lookup_field = 'pk'
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.AllowAny]
    

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    
class ClientProfileGetView(generics.ListAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class TalentProfileGetView(generics.ListAPIView):
    queryset = TalentProfile.objects.all()
    serializer_class = TalentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientProfileGetUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    lookup_field = 'pk'

    def clientprofile_update(self,serializer):
        instance = serializer.save()

class TalentProfileGetUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TalentProfile.objects.all()
    serializer_class = TalentProfileSerializer
    lookup_field = 'pk'

    def talentprofile_update(self,serializer):
        instance = serializer.save()

class SkillGetUpdateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            pk = self.kwargs['pk']
            profile = TalentProfile.objects.get(id=pk)
            skills = serializer.validated_data.get('skill_list').get('skills')
            new_skills = []
            for skill in skills:
                c_skill = Skills.objects.create(skill=skill, talent_profile=profile)
                new_skills.append(c_skill)
                c_skill.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        



class GalleryGetUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer




class QuestionGetUpdateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            pk = self.kwargs['pk']
            profile = TalentProfile.objects.get(id=pk)
            questions = serializer.validated_data.get('question_list').get('question')
            new_question = []
            for question in questions:
                freq_a_question = Question.objects.create(question=question, talent_profile=profile)
                freq_a_question.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    








class DocumentApi(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        data = {}
        for item in urls.urlpatterns:
            name = ' '.join(item.name.split('_'))
            data[name.capitalize()] = str(item.pattern)
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

   

class PayApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            api_key = 'LIVE;PK;eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBJZCI6IjY1YjI2Mzg4ZmYyYjY3MDAzYWNjOWIxNSIsInVzZXJJZCI6IjY1YjI2Mzg4ZmYyYjY3MDAzYWNjOWIxMCIsImlhdCI6MTcwNjE4OTcwNH0.xGKx2lCzKzz8kl2A4Fnns16tuzF0XSOI0ui9BVNeH-E'
            target_endpoint = 'https://api.100pay.co/api/v1/pay/charge'
            data = {
            "ref_id": "012232",
            "customer": {
                "user_id": str(request.user.id),
                "name": request.user.fullname,
                "phone": "80123456789",
                "email": request.user.email
            },
            "billing": {
                "description": "MY TEST PAYMENT",
                "amount": "10000",
                "country": "NG",
                "currency": "NGN",
                "vat": "10",
                "pricing_type": "fixed_or_partial_price"
            },
            "metadata": {
                "is_approved": "yes"
            },
            "call_back_url": "http://localhost:8000/verify-payment",
            "userId": str(request.user.id),
            "charge_source": "api"
            }
            response = requests.post(target_endpoint, json=data, headers={'api-key': f'Bearer {api_key}'})
            return Response(response.json())
        except Exception as e:
            print(f"Error making API request: {e}")
            return Response({'error': 'Internal Server Error'}, status=500)
        

class VerifyAPIView(APIView):
    pass
        
           
