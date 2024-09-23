from django.db import models
from core.models import TalentProfile, ClientProfile


class Wallet(models.Model):
    earnings = models.PositiveBigIntegerField()
    withdrawable_balance = models.PositiveBigIntegerField()
    owner = models.ForeignKey(TalentProfile, on_delete=models.CASCADE)
    pin = models.IntegerField()


    def __str__(self):
        return f"{self.owner} wallet"


class Payment(models.Model):
    network = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    transaction_id = models.CharField(max_length=500)
    timestamp = models.CharField(max_length=500)
    value = models.JSONField(blank=True, null=True)
    client_id = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    talent_id = models.ForeignKey(TalentProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"



class Withdrawal(models.Model):
    amount = models.PositiveBigIntegerField()
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)



class AllTimeEarnings(models.Model):
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)

    def __str__(self):
        return self.wallet.owner.user.fullname




class Transacions(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.description



