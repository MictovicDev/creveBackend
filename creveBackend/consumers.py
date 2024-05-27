# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from asgiref.sync import async_to_sync
# from django.db.models import Q
# from channels.layers import get_channel_layer
# # from core.models import *
# import json

# class ClientNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("clientnotifications", self.channel_name)
#         print(self.scope["user"])
#         from core.models import ClientNotification, ClientProfile, User
#         user = self.scope["user"]
#         # uls
        
#         clientprofile = ClientProfile.objects.get(user=user)  
#         clientnotification_data = ClientNotification.objects.filter(owner=clientprofile)
#         notification_data = [{
#                 'title': notification.title,
#                 'date': notification.date.strftime('%Y-%m-%d %H:%M:%S')} for notification in clientnotification_data]
#         event = notification_data
#         await self.send_notification(event)



#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("clientnotifications", self.channel_name)
        

#     async def receive(self, text_data):
#         # Handle incoming WebSocket messages
#         pass

#     async def send_notification(self, event):
#         notification = event
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'notification': notification
#         }))
        
#     async def send_client_notification(self, event):
#         #to access the the notificaton sent by the event
#         notification = event['notification']
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'notification': notification
#         }))

    

  


# class TalentNotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await self.channel_layer.group_add("talentnotifications", self.channel_name)
#         print(self)
#         from core.models import TalentNotification
#         talentnotification_data = TalentNotification.objects.all()
#         notification_data = [ {
#                 'title': notification.title,
#                 'date': notification.date.strftime('%Y-%m-%d %H:%M:%S') } for notification in talentnotification_data]
#         event = notification_data
#         await self.send_notification(event)

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("talentnotifications", self.channel_name)
        

#     async def receive(self, text_data):
#         # Handle incoming WebSocket messages
#         pass

#     async def send_notification(self, event):
#         notification = event
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'notification': notification
#         }))

    
#     async def send_talent_notification(self, event):
#         # Send notification message to the WebSocket group
#         notification = event['notification']
#         await self.send(text_data=json.dumps({
#             'type': 'notification',
#             'notification': notification
#         }))

   


# class ChatConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         await self.accept()
#         user = self.scope["user"]
#         receiver = self.scope['url_route']['kwargs']['pk']
#         from core.models import User
#         from chat.models import Chat, Message
#         chats = Chat.objects.filter(sender=user)
#         chat_data = [{
#                 'receiver_name': chat.reciever.fullname,
#                 'date': chat.date.strftime('%Y-%m-%d %H:%M:%S'),
#                 'reciever_id': str(chat.reciever.id),
                
#                 }  for chat in chats]
#         event = chat_data
#         await self.get_chat(event)
#         # await self.all_messages(user)
    
        
#     async def get_chat(self, event):
#         chats = event
#         await self.send(text_data=json.dumps({
#             'type': 'chats',
#             'chats': chats
#         }))


#     # async def all_messages():
#     #     # print(user)
#     #     # user = self.scope["user"]
#     #     # receiver = self.scope['url_route']['kwargs']['pk']
#     #     from core.models import User
#     #     from chat.models import Chat

#     #     receiver = User.objects.get(id=receiver)
#     #     chat = Chat.objects.filter(Q(sender=user, reciever=receiver) | Q(sender=receiver, reciever=user))
#     #     if chat.exists() == False:
#     #         chat = Chat.objects.create(sender=user, reciever=receiver)
#     #         await self.channel_layer.group_add(str(chat), self.channel_name)
#     #     else:
#     #         st_chat = str(chat[0])
#     #         await self.channel_layer.group_add(st_chat, self.channel_name)
#     #     messages = chat[0].messages.all()
#     #     database_messages = [ {
#     #             'body': message.body,
#     #             'date': message.date.strftime('%Y-%m-%d %H:%M:%S') } for message in messages]
#     #     await self.send(text_data=json.dumps({
#     #         'type': 'chats',
#     #         'chats': database_messages
#     #     }))


       
    
#     async def disconnect(self, close_code):
#         user = self.scope["user"]
#         receiver = self.scope['url_route']['kwargs']['pk']
#         print(receiver)
#         print(user)
#         from core.models import User
#         from chat.models import Chat, Message
#         chat = Chat.objects.filter(Q(sender=user, reciever=receiver) | Q(sender=receiver, reciever=user))
#         if chat.exists() == False:
#             chat = Chat.objects.create(sender=user, reciever=receiver)
        # await self.channel_layer.group_discard(str(chat), self.channel_name)
        

    # async def receive(self, text_data):
    #     print(text_data)
        # Handle incoming WebSocket messages
        # pass

# gunicorn creveBackend.wsgi:application