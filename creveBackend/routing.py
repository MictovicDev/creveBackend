# routing.py
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path
# from creveBackend import consumers

# websocket_urlpatterns = [
#     path('ws/chat/', consumers.ChatConsumer.as_asgi()),
#     # Add other WebSocket URL patterns here
# ]

# application = ProtocolTypeRouter({
#     'websocket': URLRouter(websocket_urlpatterns),
#     # Add other protocol routers here
# })

# routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from core import consumers

websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    # Add other WebSocket URL patterns here
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
    # Add other protocol routers here
})

