from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,PermissionsMixin)
import uuid
from .managers import UserManager




class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('Client', 'Client'),
        ('Creative', 'Creative'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=250,blank=True, null=True)
    email = models.EmailField(verbose_name='email address',max_length=255,unique=True,)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(max_length= 250, blank=True,null=True, choices=ROLE_CHOICES)
    token = models.CharField(max_length=500, blank=True, null=True)
    otp = models.CharField(max_length=500, blank=True, null=True)
    otp_secret = models.CharField(max_length=500, blank=True, null=True)
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
    




# class Profile(models.Model):

#     class Meta:
#         abstract = True

    
class TalentProfile(models.Model):
    worktype = (
        ('Remote', 'Remote'),
        ('On-site', 'On-site'),
        ('Hybrid', 'Hybrid'),
    )
    NonDigitalSkills = (
        ('Plumbing','Plumbing'),
        ('Catering','Catering'),
        ('Hair_Stylist','Hair_Stylist'),
        ('Electronics/Repairs', 'Electronics/Repairs'),
        ('Furniture-Making','Furniture-Making'),
        ('Cobbling','Cobbling'),
        ('Mechanic', 'Mechanic'),
        ('Fashion-Designer','Fashion-Designer'),
    )
    DigitalSkills = (
        ('BackendDevelopment', 'BackendDevelopment'),
        ('MobileDevelopment','MobileDevelopment'),
        ('UI/UX_Design','UI/UX_Design'),
        ('Graphics_Design','Graphics_Design'),
        ('Content_Creation','Content_Creation'),
        ('Frontend_Development', 'Frontend_Development')
    )
    CATEGORY_TYPE = (
        ('DigitalSkills', 'DigitalSkills'),
        ('Non-DigitalSkills', 'Non-DigitalSkills'),
    )
    digital_skills = models.CharField(max_length=250, choices=DigitalSkills,blank=True)
    work_type = models.CharField(max_length=500, blank=True, choices=worktype)
    verified = models.BooleanField(default=False)
    cover_image = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    summary_of_profile = models.TextField(blank=True, null=True)
    starting_price = models.PositiveBigIntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=250, blank=True, default="")
    about = models.CharField(max_length=400, blank=True, null=True)
    nondigital_skills = models.CharField(max_length=250, choices=NonDigitalSkills, blank=True)
    display_name = models.CharField(max_length=100,blank=True, null=True)
    category = models.CharField(max_length=250, blank=True, choices=CATEGORY_TYPE)
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='default.png')
    location = models.CharField(max_length=250,blank=True, null=True)
    language = models.CharField(max_length=250,blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='talentprofile')
    whatsapp_link = models.CharField(max_length=250,blank=True, default="")
    website_link = models.CharField(max_length=250, blank=True, default="")
    resume_link = models.URLField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.user.fullname}'s  Profile"
    


class Gallery (models.Model):
    image = models.ImageField(upload_to='files/images',blank=True, null=True)
    talentprofile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True, null=True,related_name="images")

    def __str__(self):
        return f"{self.talentprofile.user.fullname}'s  Gallery"



class Skill(models.Model):
    skill = models.CharField(max_length=250, blank=True, null=True)
    talentprofile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True, null=True,related_name="dskills")
        
    def __str__(self):
        return f"{self.talentprofile.user.fullname}'s  Skills"




class ClientProfile(models.Model):
    profile_pics = models.ImageField(upload_to='files/images', blank=True, null=True, default='files/images/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='clientprofile')


    def __str__(self):
        return f"{self.user.fullname}'s  Profile"
    

class BookedCreative(models.Model):
    talent_profile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True, null=True,related_name='books')
    client_profile = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, blank=True,null=True)
    title = models.CharField(max_length=250, null=True)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=250, null=True)


    def __str__(self):
        return f"{self.client_profile.user.fullname} booked {self.talent_profile.user.fullname}"
      


    
class ClientNotification(models.Model):
    owner = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name='clientnotification', blank=True, null=True)
    title = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.title
    
class TalentNotification(models.Model):
    owner = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, related_name='talentnotification', blank=True, null=True)
    title = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)



    class Meta:
        ordering = ['-date']


    def __str__(self):
        return self.title
    



class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length=250, blank=True, null=True)
    reviewer = models.ForeignKey(ClientProfile, on_delete=models.CASCADE,related_name='reviews')
    reviewed = models.ForeignKey(TalentProfile, on_delete=models.CASCADE,null=True,related_name='reviewed')





class Question(models.Model):
    question = models.CharField(max_length=5000, blank=True, null=True)
    answer = models.TextField(blank=True,null=True)
    talent_profile = models.ForeignKey(TalentProfile, on_delete=models.CASCADE, blank=True, null=True, related_name='questions')


    def __str__(self):
        return self.question


    

