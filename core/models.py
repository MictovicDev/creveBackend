from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)
import uuid
from .managers import UserManager
from django.contrib.postgres.fields import ArrayField


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Client', 'Client'),
        ('Talent', 'Talent'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=250,blank=True, null=True)
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
    



class Skills(models.Model):
    skill = models.CharField(max_length=250, blank=True, null=True)


class Gallery (models.Model):
    image = models.ImageField(upload_to='files/images',blank=True, null=True)
    

    def __str__(self):
        return self.image.url



class TalentProfile(models.Model):
    worktype = (
        ('Remote', 'Remote'),
        ('On-site', 'On-site'),
        ('Hybrid', 'Hybrid'),
    )
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
    work_type = models.CharField(max_length=500, blank=True, null=True, choices=worktype)
    verified = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skills)
    images = models.ManyToManyField(Gallery)
    cover_image = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    summary_of_profile = models.TextField(blank=True, null=True)
    starting_price = models.PositiveBigIntegerField(blank=True, null=True)
    about = models.CharField(max_length=250, blank=True, null=True)
    nondigital_skills = models.CharField(max_length=250, choices=NonDigitalSkills, blank=True, null=True)
    display_name = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=250, blank=True, null=True, choices=CATEGORY_TYPE)
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    location = models.CharField(max_length=250,blank=True, null=True)
    language = models.CharField(max_length=250,blank=True, null=True)
    phone_number = models.CharField(max_length=250, blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='talentprofile')
    whatsapp_link = models.URLField(blank=True, null=True)
    resume_link = models.URLField(blank=True, null=True)
    website_link = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.fullname}'s  Profile"
    

    
    
 
    # talent_profile = models.ForeignKey(TalentProfile, blank=True, null=True, on_delete=models.CASCADE, related_name='skills')
    

class ClientProfile(models.Model):
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='files/images/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clientprofile')


    def __str__(self):
        return f"{self.user.fullname}'s  Profile"
    
class ClientNotification(models.Model):
    owner = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='clientnotification', blank=True, null=True)
    title = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.title
    
class TalentNotification(models.Model):
    title = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.title
    



class Review(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='files/images',blank=True, null=True)
    reviewer = models.ForeignKey(ClientProfile, on_delete=models.CASCADE,blank=True, null=True)
    reviewed = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True, null=True,related_name='reviewed')
    relevant_link = models.URLField(blank=True, null=True)





class Question(models.Model):
    question = models.CharField(max_length=5000, blank=True, null=True)
    answer = models.TextField(blank=True,null=True)
    talent_profile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True, null=True, related_name='questions')


    def __str__(self):
        return self.question


# class WorkType(models.Model):
    
#     work_type = models.CharField(max_length=250, blank=True, null=True, choices=worktype_choice)
#     profile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE,related_name='work_type')

#     def __str__(self):
#         return self.work


# class Notification(models.Model):
    

    


# class WorkSchedule(models.Model):
#     day_choices = [
#         ('Sunday', 'Sunday'),
#         ('Monday', 'Monday'),
#         ('Tuesday', 'Tuesday'),
#         ('Wednesday', 'Wednesday'),
#         ('Thursday', 'Thursday'),
#         ('Friday', 'Friday'),
#         ('Saturday', 'Saturday')
#     ]


#     day = models.CharField(max_length=500, blank=True, null=True, choices=day_choices)
#     start_time = models.TimeField()
#     end_time = models.TimeField()
#     talent_profile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True,null=True, related_name='work_schedule')

#     def __str__(self):
#         return f"{self.day} - {self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p').replace('AM', 'PM')}"

    

