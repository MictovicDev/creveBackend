from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
       if not (email):
           raise ValueError('User must have an email address')
       
       email = self.normalize_email(email)
       user = self.model(email=self.normalize_email(email),**extra_fields)
       
       user.set_password(password)
       user.is_active = True
       user.save(using=self.db)
       return user
        

#    /
#https://localhost:8000/oauth/complete/google-oauth2/
    def create_superuser(self, email,password=None,**extra_fields):
        user = self.create_user(email,password,**extra_fields)
        user.is_admin=True
        
        user.save(using=self.db)
        return user