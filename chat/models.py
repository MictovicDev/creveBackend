from django.db import models
from core.models import User

# Create your models here.
class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Chat betweeen {self.sender} and {self.receiver}"
    
    


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.body[0:20]
    
