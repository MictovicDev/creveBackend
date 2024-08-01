from core.models import *
from rest_framework import serializers
from rest_framework.response import Response
from core.serializers import *
from chat.models import *


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    chat = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    sender = UserSerializer(required=False)
    reciever = UserSerializer(required=False)
    class Meta:
        model = Message
        fields = '__all__'



class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(required=False, many=True,read_only=True)
    sender = TalentProfileSerializer(required=False)
    reciever = ClientProfileSerializer(required=False)
   
    class Meta:
        model = Chat
        fields = '__all__'