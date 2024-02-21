from core.models import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers,response,status
from django.contrib.auth.password_validation import validate_password
from core.models import *
from phonenumber_field.serializerfields import PhoneNumberField
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
      elif user.role == 'Talent':
         profile_pics = user.talentprofile.profile_pics.url
         token['profile_id'] = user.talentprofile.id
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
     user = serializers.PrimaryKeyRelatedField(read_only=True)
     class Meta:
         model = ClientProfile
         fields = ('id','user','profile_pics',)

class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False,read_only=True)
    skill_list = serializers.JSONField(write_only=True)

    class Meta:
        model = Skills
        fields = ('id','skill','skill_list')

    

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('images',)

class QuestionSerializer(serializers.ModelSerializer):
    question_list = serializers.JSONField(write_only=True)
   #  question = serializers.
    class Meta:
        model = Question
        fields = ['id', 'question','question_list']

class WorkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkType
        fields = ('work_type',)

class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = '__all__'

class PhoneNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(region="CA")

class TalentProfileSerializer(serializers.ModelSerializer):
     skills = SkillSerializer(read_only=True,many=True)
     gallery = GallerySerializer(read_only=True)
     questions = QuestionSerializer(read_only=True,many=True)
     work_type = WorkTypeSerializer(read_only=True,many=True)
     work_schedule = WorkScheduleSerializer(many=True, required=False)
     phone_number = PhoneNumberSerializer()
     user = serializers.PrimaryKeyRelatedField(read_only=True)


     class Meta:
         model = TalentProfile
         fields = '__all__'
      
    
         
class UserUpdateSerializer(serializers.ModelSerializer):
     id = serializers.UUIDField(read_only=True,)
     email = serializers.EmailField(read_only=True)
     fullname = serializers.CharField()
     

     class Meta:
        model = User
        fields = ('id','email','fullname',)

class TalentUpdateSerializer(serializers.ModelSerializer):
     id = serializers.UUIDField(read_only=True,)
     email = serializers.EmailField(read_only=True)
     fullname = serializers.CharField()
     

     class Meta:
        model = User
        fields = ('id','email','fullname',)
    

    
     
