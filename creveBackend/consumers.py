# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
# from core.models import *
from core.views import notfi
import json

class ClientNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        # Accept the WebSocket connection
        await self.channel_layer.group_add("clientnotifications", self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("clientnotifications", self.channel_name)
        

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass

    
    async def send_client_notification(self, event):
        # Send notification message to the WebSocket group
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

  


class TalentNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        # Accept the WebSocket connection
        await self.channel_layer.group_add("talentnotifications", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("talentnotifications", self.channel_name)
        

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass

    
    async def send_talent_notification(self, event):
        # Send notification message to the WebSocket group
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))

   
    


# gunicorn creveBackend.wsgi:application