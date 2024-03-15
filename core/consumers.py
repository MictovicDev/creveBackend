# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from core.models import *
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        # Accept the WebSocket connection
        await self.accept()
        await self.channel_layer.group_add("notifications", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("notifications", self.channel_name)
        

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass

    @database_sync_to_async
    def get_latest_client_notification(self):
        # Retrieve the latest notification from the database
        return ClientNotification.objects.latest('date')
    

    @database_sync_to_async
    def get_latest_talent_notification(self):
        # Retrieve the latest notification from the database
        return TalentNotification.objects.latest('date')
    
    async def send_client_notification(self, event):
        # Send notification message to the WebSocket group
        notification = event['notification']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification': notification
        }))
    


# gunicorn creveBackend.wsgi:application