from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
# from core.models import *
import json

class ClientNotificationConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("connected")
        await self.channel_layer.group_add("clientnotifications", self.channel_name)
        result = await self.send_notification()
        print(result)
        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("clientnotifications", self.channel_name)
        

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass

    @database_sync_to_async
    def get_my_data(self):
        from core.models import ClientNotification
        client = ClientNotification.objects.all()
        return client
    
    async def send_notification(self):
        from core.models import ClientNotification
        channel_layer = get_channel_layer()
        clientnotification_data = ClientNotification.objects.all()
        notifications_data = []
        for notification in clientnotification_data:
            notification_dict = {
                'title': notification.title,
                'date': notification.date.strftime('%Y-%m-%d %H:%M:%S')  # Convert date to string in desired format
            }
            notifications_data.append(notification_dict)
        channel_layer.group_send(
            "clientnotifications",
            {
                'type': 'send_client_notification',
                'notification': notification
            }
        )
        return notifications_data
      
        
    async def send_client_notification(self, event):
        #to access the the notificaton sent by the event
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