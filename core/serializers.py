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
         fields = ('profile_pics',)

class UpdateClientSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    clientprofile = ClientProfileSerializer(required=False)
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ('clientprofile','email','id','fullname')
    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
        profile_data = validated_data.get('clientprofile')
        print(profile_data)
        if profile_data:
            profile_instance = instance.clientprofile
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            profile_instance.save()
        instance.save()
        return instance
    

    
     
class TalentProfileSerializer(serializers.ModelSerializer):
     class Meta:
         model = TalentProfile
         fields = ('profile_pics','display_name','location','language','about')
         
     def update(self, instance, validated_data):
         instance.profile_pics = validated_data.get('profile_pics')
         instance.dispaly_name = validated_data.get('display_name')
         instance.location = validated_data.get('location')
         instance.language = validated_data.get('language')
         instance.about = validated_data.get('about')
         instance.save()
         return instance