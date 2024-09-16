from django.db import models
from core.models import TalentProfile, ClientProfile
from shortuuidfield import ShortUUIDField

# Create your models here.

class Transaction(models.Model):
    status = (
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Failed', 'Failed'),
    )
    uuid = ShortUUIDField()
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    creative = models.ForeignKey(TalentProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, choices=status, default='Pending')

    def __str__(self):
        return(f"Transaction between {self.client} and {self.user}")
    

