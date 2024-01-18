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
    fullname = models.CharField(max_length=250,blank=True, null=True)
    phone_number = models.PositiveBigIntegerField(null=True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
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
    NonDigitalSkills = (
        ('Plumber','Plumber'),
        ('Civil-Engineer', 'Civil-Engineer'),
        ('Catering','Catering'),
        ('Hair_Stylist','Hair_stylist'),
        ('Electronics/Repairs', 'Electronics/Repairs'),
        ('Upholstery','Uphosltery'),
        ('Cobbling','Cobbling'),
        ('Mechanic', 'Mechanic'),
        ('Fashion-Designer','Fashion-Designer'),
    )
    DigitalSkills = (
        ('BackendDevelopment', 'BackendDevelopment'),
        ('MobileDevelopment','MobileDevelopment'),
        ('UI/UX_Design','UI/UX_Design'),
        ('Branding_and_Printing', 'Branding_and_Printing'),
        ('Graphics_Design','Graphics_Design'),
        ('Content_Creation','Content_Creation'),
        ('Frontend_development', 'Frontend_Development')
    )
    CATEGORY_TYPE = (
        ('DigitalSkills', 'DigitalSkills'),
        ('Non-DigitalSkills', 'Non-DigitalSkills'),
    )
    digital_skills = models.CharField(max_length=250, choices=DigitalSkills,blank=True, null=True)
    nondigital_skills = models.CharField(max_length=250, choices=NonDigitalSkills, blank=True, null=True)
    display_name = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=250, blank=True, null=True, choices=CATEGORY_TYPE)
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    location = models.CharField(max_length=250,blank=True, null=True)
    language = models.CharField(max_length=250,blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='talentprofile')


    def __str__(self):
        return f"{self.user.fullname}'s  Profile"
    
    
# class DigitalSkill(models.Model):
#     SKILLS_CHOICES = (
#         ('BackendDevelopment', 'BackendDevelopment'),
#         ('MobileDevelopment','MobileDevelopment'),
#         ('UI/UX_Design','UI/UX_Design'),
#         ('Branding_and_Printing', 'Branding_and_Printing'),
#         ('Graphics_Design','Graphics_Design'),
#         ('Content_Creation','Content_Creation'),
#         ('Frontend_development', 'Frontend_Development')
#     )
#     skills = models.CharField(max_length=250, blank=True, null=True, choices=SKILLS_CHOICES)
#     talentprofile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE,related_name='digital_skills')


# class NonDigitalSkill(models.Model):
#     SKILLS_CHOICES = (
#         ('Plumber','Plumber'),
#         ('Civil-Engineer', 'Civil-Engineer'),
#         ('Catering','Catering'),
#         ('Hair_Stylist','Hair_stylist'),
#         ('Electronics/Repairs', 'Electronics/Repairs'),
#         ('Upholstery','Uphosltery'),
#         ('Cobbling','Cobbling'),
#         ('Mechanic', 'Mechanic'),
#         ('Fashion-Designer','Fashion-Designer'),
#     )
#     skills = models.CharField(max_length=250, blank=True, null=True, choices=SKILLS_CHOICES)
#     talentprofile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE,related_name='non_digitalskills')






class ClientProfile(models.Model):
    
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clientprofile')


    def __str__(self):
        return f"{self.user.fullname}'s  Profile"
    

