from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework import generics,permissions,status, response
from rest_framework.decorators import api_view, renderer_classes
from chat.models import *
from chat.serializers import *
from core.models import *
from chat.pusher import pusher_client
from core.models import *
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from core import email






def inbox(request, room_name):
    user = request.user
    if user.role == 'Client':
        profile = user.clientprofile
        chats = Chat.objects.filter(sender=profile)
        # chat = Chat.objects.get(sender=profile, reciever=talent_profile)
        chat = Chat.objects.get(room_name=room_name)
        recipient = chat.reciever
    else:
        profile = user.talentprofile
        chats = Chat.objects.filter(reciever=profile)
        chat = Chat.objects.get(room_name=room_name)
        # talent_profile = TalentProfile.objects.get(id=user_id)
        recipient = chat.sender
    print(recipient)
    print(chat)
    # pusher_client.trigger(chat.room_name, 'message', {"message":f"Connected {chat.room_name}"})
    messages = Message.objects.filter(chat=chat)
    # print(messages)
    context = {
        'user': user,
        'chats': chats,
        'chat_room': chat.room_name,
        'messages': messages,
         'user': user,
        'talent_profile': recipient.user.fullname
    }
    return render(request, 'chat/chatting.html', context)

def send_message(request, user_id):
    if request.method == 'POST':
        print(user_id)
        message = request.POST.get('message')
        print(message)
        # recipient_id = request.POST.get('recipient_id')
        return redirect('chats',user_id)
    return HttpResponse("Invalid request", status=400)


def creative(request):
    creatives = TalentProfile.objects.all()
    print(creatives)
    context = {
        "creatives": creatives
    }
    return render(request, 'chat/creativepage.html', context)


class MessageView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        room_name = self.kwargs.get('room_name')
        try:
            chat = Chat.objects.get(room_name=room_name)
            return Message.objects.filter(chat=chat)
        except Chat.DoesNotExist:
            return response.Response({"message":"Chat Does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        room_name = self.kwargs.get('room_name')
        try:
            chat = Chat.objects.get(room_name=room_name)
            user = request.user
            # client_profile = user.clientprofile
            pusher_client.trigger(chat.room_name, 'connected',{'message': 'connected_successfully'})
            messages = chat.messages.all()
            serializer = MessageSerializer(instance=messages, many=True)
            return response.Response(serializer.data, status=status.HTTP_200_OK) #return for the Api
        except Chat.DoesNotExist:
            return response.Response({"message":"Chat Does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request, *args, **kwargs):
        room_name = self.kwargs.get('room_name')
        try:
            chat = Chat.objects.get(room_name=room_name)
            print(chat.sender.user.email)
            if chat.sender.user.email == request.user.email:
                sender = request.user
                reciever = chat.reciever.user
            else:
                sender = chat.reciever.user
                reciever = chat.sender.user
            pusher_client.trigger(chat.room_name, 'message', {'message': {"body": request.data.get('body'), "sender": sender.email, 'reciever': reciever.email, "fullname":sender.fullname, "room_name": chat.room_name}})
            message = Message.objects.create(
                                    chat=chat,
                                    sender=sender,
                                    reciever=reciever, 
                                    body=request.data.get('body'))
            serializer = MessageSerializer(instance=message)
            print(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return response.Response({"message":f"Error {e}"})




class AllChatView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Client':
            profile = user.clientprofile
            return Chat.objects.filter(sender=profile)
        else:
            profile = user.talentprofile
            return Chat.objects.filter(reciever=profile)



class ChatView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Client':
            profile = user.clientprofile
            return Chat.objects.filter(sender=profile)
        else:
            profile = user.talentprofile
            return Chat.objects.filter(reciever=profile)
            
            # talent_profile = TalentProfile.objects.get(id=user_id)


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                pk = self.kwargs.get('pk')
                try:
                    talent_profile = TalentProfile.objects.get(id=pk)
                except TalentProfile.DoesNotExist:
                    return response.Response({"message": "TalentProfile Does not exist"})
                user = request.user
                print(user.role)
                if  user.role == 'Client':
                    try:
                        profile_id = user.clientprofile.id
                        client_profile = ClientProfile.objects.get(id=profile_id)
                        chat, created= Chat.objects.get_or_create(sender=client_profile, reciever=talent_profile, room_name=f"chat_inbox_{talent_profile.id}_{client_profile.id}_unique")
                        talent_user = talent_profile.user
                        Message.objects.create(
                                    chat=chat,
                                    sender=request.user,
                                    reciever=talent_user, 
                                    body=request.data.get('body'))
                        email.message_sent_mail(fullname=talent_profile.user.fullname, clientname=client_profile.user.fullname, useremail=talent_profile.user.email, message=request.data.get('body')[0:10])
                        serializer = ChatSerializer(instance=chat)
                        return response.Response(serializer.data, status=status.HTTP_200_OK)
                    except Exception as e:
                        return response.Response({"message":f"error {e}"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return response.Response({"message": "Creative cannot initialize chat"})
            except Exception as e:
              return response.Response({"message": "User not authenticated"}, status=status.HTTP_400_BAD_REQUEST)
        return response.Response({"message":"Create"}, status=status.HTTP_200_OK)
    
        

   

    