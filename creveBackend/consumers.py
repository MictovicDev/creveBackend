from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# from core.models import *
import json

class ClientNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("clientnotifications", self.channel_name)
        print(self.scope["user"])
        from core.models import ClientNotification, ClientProfile, User
        user = self.scope["user"]
        # uls
        
        clientprofile = ClientProfile.objects.get(user__id=user_pk)  
        clientnotification_data = ClientNotification.objects.filter(owner=clientprofile)
        notification_data = [{
                'title': notification.title,
                'date': notification.date.strftime('%Y-%m-%d %H:%M:%S')} for notification in clientnotification_data]
        event = notification_data
        await self.send_notification(event)



    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("clientnotifications", self.channel_name)
        

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass

    async def send_notification(self, event):
        notification = event
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
        
    async def send_client_notification(self, event):
        #to access the the notificaton sent by the event
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

    

  


class TalentNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("talentnotifications", self.channel_name)
        print(self)
        from core.models import TalentNotification
        talentnotification_data = TalentNotification.objects.all()
        notification_data = [ {
                'title': notification.title,
                'date': notification.date.strftime('%Y-%m-%d %H:%M:%S') } for notification in talentnotification_data]
        event = notification_data
        await self.send_notification(event)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("talentnotifications", self.channel_name)
        

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass

    async def send_notification(self, event):
        notification = event
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

    
    async def send_talent_notification(self, event):
        # Send notification message to the WebSocket group
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

   


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user_pk = self.scope["user"].pk
        user = self.scope["user"]
        print(self.scope['url_route']['kwargs']['pk'])
        print(user)
        from core.models import User
        from chat.models import Chat, Message
        sender = User.objects.get(id)
        # chat = Chat.objects.filter(sender=)
        # await self.channel_layer.group_add("talentnotifications", self.channel_name)


# gunicorn creveBackend.wsgi:application