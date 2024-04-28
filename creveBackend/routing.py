
from django.urls import path, re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .consumers import *

websocket_urlpatterns = [
    path('ws/clientnotifications/', ClientNotificationConsumer.as_asgi()),
    path('ws/talentnotifications/', TalentNotificationConsumer.as_asgi()),
    re_path(r'ws/chats/(?P<pk>[\w-]+)/$',ChatConsumer.as_asgi()),
]

print(websocket_urlpatterns[-1].pattern)

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})



