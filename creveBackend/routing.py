
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import *

websocket_urlpatterns = [
    path('ws/clientnotifications/<str:pk>/', ClientNotificationConsumer.as_asgi()),
    path('ws/talentnotifications/', TalentNotificationConsumer.as_asgi()),
    path('ws/chats/<str:pk/', ChatConsumer.as_asgi()),

]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})



