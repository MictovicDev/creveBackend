from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)
import uuid
from .managers import UserManager
# from core.models import Project



# from django_phonenumbers import PhoneNumber


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Client', 'Client'),
        ('Talent', 'Talent'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.PositiveBigIntegerField(null=True)
    lastname = models.CharField(max_length=500)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    fullname = models.CharField(max_length=50, blank=True, null=True,unique=False)
    role = models.CharField(max_length= 250, blank=True,null=True, choices=ROLE_CHOICES)
    token = models.CharField(max_length=500, blank=True, null=True)
    updates = models.BooleanField(default=False)
    authMedium = models.CharField(max_length=50, default='email')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname','role']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    


class TalentProfile(models.Model):
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    display_name = models.CharField(max_length=100,blank=True, null=True)
    location = models.CharField(max_length=250,blank=True, null=True)
    language = models.CharField(max_length=250,blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='talentprofile')



class ClientProfile(models.Model):
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    name = models.CharField(max_length=100,blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clientprofile')