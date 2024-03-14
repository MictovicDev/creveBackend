# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Clean up when the WebSocket is closed
        pass

    async def receive(self, text_data):
        # Handle incoming WebSocket messages
        pass


# gunicorn creveBackend.wsgi:application