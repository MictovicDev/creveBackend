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


class QuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['id', 'question','answer']


class GallerySerializer(serializers.ModelSerializer):
    images_list = serializers.ListField(required=False, write_only=True)
    image = serializers.ImageField(required=False)
    class Meta:
        model = Gallery
        fields = ('id','image','images_list')


class NinSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Nin
        fields = ('id', 'image')


class ActivationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('email','otp',)



class UserSerializer(serializers.ModelSerializer):
     password = serializers.CharField(write_only=True, required=True)
     id = serializers.UUIDField(read_only=True,)
     role = serializers.CharField()
     fullname = serializers.CharField()
    #  talentprofile = TalentProfileSerializer(read_only=True)
     
     

     class Meta:
        model = User
        fields = ('id','email','password','fullname','role')


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
     

class OTPSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email',)


     

class ClientProfileSerializer(serializers.ModelSerializer):
     user = UserSerializer(read_only=True)
     class Meta:
         model = ClientProfile
         fields = ('id','user','profile_pics','address')


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = ClientProfileSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id','content','reviewer','rating']


class TalentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TalentProfile
        fields = ('id','profile_pics','user','nin')

class VerificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Verification
        fields = '__all__'


class BookedCreativeSerializer(serializers.ModelSerializer):
    talent_profile = TalentSerializer(read_only=True)
    client_profile = ClientProfileSerializer(read_only=True)
    class Meta:
        model = BookedCreative
        fields = ('id','title', 'description', 'client_profile','phone','talent_profile')

class TalentProfileSerializer(serializers.ModelSerializer):
     dskills = SkillSerializer(read_only=True, many=True)
     images = GallerySerializer(read_only=True,many=True)
     user = UserSerializer(read_only=True)
     books = BookedCreativeSerializer(read_only=True, many=True)
     reviewed = ReviewSerializer(read_only=True, many=True)
     questions = QuestionSerializer(read_only=True, many=True)
     verification = VerificationSerializer(read_only=True)


     class Meta:
        model = TalentProfile
        fields = '__all__'

class AdminCreativeSerializer(serializers.ModelSerializer):
    verification = VerificationSerializer()
    nin = NinSerializer()
    class Meta:
        model = TalentProfile
        fields = ['id','profile_pics','display_name', 'cover_image', 'verification','is_banned','nin']



         
class UserUpdateSerializer(serializers.ModelSerializer):
     id = serializers.UUIDField(read_only=True,)
     email = serializers.EmailField(read_only=True)
     fullname = serializers.CharField()
     

     class Meta:
        model = User
        fields = ('id','email','fullname',)


class ClientNotificationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True,)
    

    class Meta:
        model = ClientNotification
        fields = ('id', 'title', 'date')



class TalentUpdateSerializer(serializers.ModelSerializer):
     id = serializers.UUIDField(read_only=True,)
     email = serializers.EmailField(read_only=True)
     fullname = serializers.CharField()
     

     class Meta:
        model = User
        fields = ('id','email','fullname',)


class WaitListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Waitlist
        fields = '__all__'
    


    
     
