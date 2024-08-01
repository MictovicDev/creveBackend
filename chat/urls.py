from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.AllChatView.as_view(), name='chats'),
    path('<int:pk>/', views.ChatView.as_view(), name='chats'),
    path('messages/<str:room_name>/', views.MessageView.as_view(), name='message'),
    path('send-message/<user_id>/', views.send_message, name='send_message'),
    path('inbox/<str:room_name>/', views.inbox, name='inbox'),
    path('creative/', views.creative, name='listcreative'),
]