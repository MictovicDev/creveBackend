from django.urls import path,include
from . import views


urlpatterns = [
    path('', views.chat, name='chat'),
    path('<str:pk>/', views.send, name='chats')
   
]