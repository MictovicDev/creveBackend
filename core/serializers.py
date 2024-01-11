from core.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers,response,status
from django.contrib.auth.password_validation import validate_password
from core.models import *
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
      elif user.role == 'Talent':
         profile_pics = user.talentprofile.profile_pics.url
      token['profile_pics'] = 'https://creve.onrender.com' + profile_pics
      return token
    

class UserSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True, required=True)
     id = serializers.UUIDField(read_only=True,)
     role = serializers.CharField(read_only=True,)
     fullname = serializers.CharField()
     

     class Meta:
        model = User
        fields = ('id','email','password','fullname','role',)

     def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
     
     def validate_password(self,attrs):
        if len(attrs) < 8:
          raise serializers.ValidationError("Password is too short.")
        if not re.search(r"[A-Z]", attrs):
            raise serializers.ValidationError("Password Should contain a capital letter.")
        if not re.search(r"[a-z]", attrs):
           raise serializers.ValidationError("Password should contain a lower letter.")
        if not re.search(r"\d", attrs):
           raise serializers.ValidationError("Password should contain a digit.")
        if not re.search(r"[!@#$%^&*]", attrs):
           raise serializers.ValidationError("Password should have a special character.")
        return attrs
     


class ClientProfileSerializer(serializers.ModelSerializer):
     class Meta:
         model = ClientProfile
         fields = ('profile_pics','name')
     def update(self,instance, validated_data):
         instance.profile_pics = validated_data.get('profile_pics')
         instance.name = validated_data.get('name')
         instance.save()
         return instance