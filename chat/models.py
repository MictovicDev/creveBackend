from django.db import models
from core.models import *

# Create your models here.
class Chat(models.Model):
    sender = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='sent_chats',null=True)
    reciever = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, related_name='received_chats',null=True)
    date = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=250, blank=True, null=True, unique=True)


    def __str__(self):
        return f"Chat_betweeen_{self.sender.id}_and_{self.reciever.id}"
    
    


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_message', null=True)
    reciever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_message', null=True)
    delivered = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.body[0:20]
    
