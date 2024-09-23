from core.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers,response,status
from django.contrib.auth.password_validation import validate_password
from core.models import *
from django.shortcuts import get_object_or_404

import re


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
      token = super().get_token(user)
      token['email'] = user.email
      token['role'] = user.role
      token['name'] = user.fullname
      if user.role == 'Client':
         profile_pics = user.clientprofile.profile_pics.url
         token['profile_id'] = user.clientprofile.id
         profile = user.clientprofile
      elif user.role == 'Creative':
         profile = user.talentprofile
         if user.talentprofile.profile_pics:
             profile_pics = user.talentprofile.profile_pics.url
         else:
             profile_pics = ''
         token['profile_id'] = user.talentprofile.id
      
      return token
    


class SkillSerializer(serializers.ModelSerializer):
    skills_list = serializers.ListField(required=False, write_only=True)
    skill = serializers.CharField(required=False)
   
    class Meta:
        model = Skill
        fields = ('id','skill','skills_list')