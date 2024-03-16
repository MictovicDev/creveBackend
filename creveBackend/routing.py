
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import ClientNotificationConsumer, TalentNotificationConsumer

websocket_urlpatterns = [
    path('ws/clientnotifications/', ClientNotificationConsumer.as_asgi()),
    path('ws/talentnotifications/', TalentNotificationConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})



