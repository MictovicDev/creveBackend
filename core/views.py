from django.shortcuts import render, redirect
from rest_framework import generics,permissions, response, status,filters
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView
from core.models import *
from . import email
from django.dispatch import receiver
import requests
from . import urls
from core.serializers import *
from django.db.models.signals import post_save
from .models import TalentProfile
from django.db.models.signals import post_save
import pyotp

# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


@receiver(post_save, sender=User)
def post_save_handler(sender, instance, created, **kwargs):
     fullname = instance.fullname
     useremail = instance.email
     otp = instance.otp
     if created:
       if instance.role == 'Client':
           email.send_linkmail(fullname,useremail,otp)
           ClientProfile.objects.create(user=instance)
       else:
          email.send_linkmail(fullname,useremail,otp)
          TalentProfile.objects.create(user=instance)





class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




#changes
class CreateUserView(generics.ListCreateAPIView):
     serializer_class = UserSerializer
     permission_classes = [permissions.AllowAny]
     queryset = User.objects.all()

     def perform_create(self, serializer):
        if serializer.is_valid():
            base32secret3232 = pyotp.random_base32()
            otp = pyotp.TOTP(base32secret3232, interval=230, digits=5)
            time_otp = otp.now()
            role = serializer.validated_data.get('role')
            otp_secret = base32secret3232
            user = serializer.save(
                otp=time_otp, role=role, otp_secret=otp_secret)
            token = str(RefreshToken.for_user(user))
            user.token = token
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






    
class TalentView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.filter(role='Talent')
    filter_backends = [filters.SearchFilter]
    search_fields = ['fullname', 'email','role']

    
    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save(role='Talent')
            proflie = TalentProfile.objects.create(user=user)
            token = str(RefreshToken.for_user(user))
            user.token = token
            fullname = user.fullname
            useremail = user.email
            user.is_active = True
            user.save()
            email.send_linkmail(fullname,useremail,token)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ActivateAccount(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ActivationSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        otp = request.data.get('otp')
        try:
            user = User.objects.get(email=email, otp=otp)
        except:
            data = {'message': "User Does not exists"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        if  pyotp.TOTP(user.otp_secret, interval=230, digits=5).verify(otp):
            user.is_active = True
            user.save()
            data = {
                'user': user.email,
                'token': user.token
            }
            return Response(data=data, status=status.HTTP_200_OK)
            # return redirect('http://localhost:8000/api/token')
            
        else:
            data = {'message': "Token has Expired"}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
            # print('False')
            # except:
            #     data = {'message': "Token has Expired"}
            #     return Response(data=data, status=status.HTTP_404_NOT_FOUND)
           
        


       
    
        



class ClientUpdateGetDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role='Client')
    lookup_field = 'pk'
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.AllowAny]
    

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    
class TalentUpdateGetDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role='Talent')
    lookup_field = 'pk'
    serializer_class = TalentUpdateSerializer
    permission_classes = [permissions.AllowAny]
    
    

    def users_update(self, serializer):
        instance = serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)

    
class ClientProfileGetView(generics.ListAPIView):
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]




class TalentProfileGetView(generics.ListAPIView):
    queryset = TalentProfile.objects.all()
    serializer_class = TalentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['category','location','phone_number','whatsapp_link','resume_link','website_link','digital_skills']


class ClientProfileGetUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ClientProfile.objects.all()
    serializer_class = ClientProfileSerializer
    lookup_field = 'pk'

    def clientprofile_update(self,serializer):
        instance = serializer.save()

class TalentProfileGetUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = TalentProfile.objects.all()
    serializer_class = TalentProfileSerializer
    lookup_field = 'pk'

    def talentprofile_update(self,serializer):
        print(serializer.validated_data)
        instance = serializer.save()

class SkillListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            pk = self.kwargs['pk']
            profile = TalentProfile.objects.get(id=pk)
            skills = serializer.validated_data.get('skill_list').get('skills')
            for skill in skills:
                c_skill = Skills.objects.create(skill=skill)
                profile.skills.add(c_skill)
                c_skill.save()
                profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ReviewCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            content = serializer.validated_data['content']
            reviewer = self.request.user
            clientprofile = ClientProfile.objects.get(user=reviewer)
            image = serializer.validated_data['image']
            relevant_link = serializer.validated_data['relevant_link']
            pk = self.kwargs['pk']
            talentprofile = TalentProfile.objects.get(id=pk)
            review = Review.objects.create(content=content,image=image, relevant_link=relevant_link, reviewer=clientprofile,reviewed=talentprofile)
            review.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            
            

class GalleryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            # pk = self.request.user.id
            print(serializer.validated_data)
            pk = self.kwargs['pk']
            profile = TalentProfile.objects.get(id=pk)
            images = serializer.validated_data.get('image_list').get('images')
            print(images)
            for image in images:
                gallery = Gallery.objects.create(image=image)
                profile.images.add(gallery)
                gallery.save()
                profile.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
                
        

class GalleryGetUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer



class QuestionUpdateDel(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = 'pk'

    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     print(pk)
    #     questions = Question.objects.filter(talent_profile__id=pk)
    #     return questions
    
    def question_update(self, serializer):
        instance = serializer.save()

    def question_destroy(self, instance):
        return super().perform_destroy(instance)

class QuestionListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # print(dir(generics.ListAPIView))
    # 
        
    def perform_create(self, serializer):
        if serializer.is_valid():
            print(self.request.user.is_authenticated)
            if self.request.user.is_authenticated:
                try:
                    user = self.request.user
                    print(user)
                    profile = TalentProfile.objects.get(user=user)
                    print(profile)
                except:
                    return Response({"message": "profile does not exist"})
            else:
                return Response({"message": "you must be logged in to create question"})
            quest = serializer.validated_data['question']
            answer = serializer.validated_data['answer']
            question = Question.objects.create(question=quest, answer=answer,talent_profile=profile)
            print(question)
            question.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
            

    



def clientnotifications(request):
    return render(request, "core/ws.html")

def talentnotifications(request):
    return render(request, "core/tl.html")


class DocumentApi(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        data = {}
        for item in urls.urlpatterns:
            name = ' '.join(item.name.split('_'))
            data[name.capitalize()] = str(item.pattern)
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)

   
# @receiver(post_save, sender=TalentProfile)
# def clientnotification(sender, instance, created, **kwargs):
#     if created:
#         ClientNotification.objects.create(title= f"A New Talent {instance.user.fullname} just joined Creve")
#         notifications_data = []
#         clientsnotification_data = ClientNotification.objects.all()
#         for notification in clientsnotification_data:
#             notification_dict = {
#                 'title': notification.title,
#                 'date': notification.date.strftime('%Y-%m-%d %H:%M:%S')  # Convert date to string in desired format
#             }
#             notifications_data.append(notification_dict)
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "clientnotifications",
#             {
#                 'type': 'send_client_notification',
#                 'notification': notifications_data
#             }
#         )

# @receiver(post_save, sender=ClientProfile)
# def talentnotification(sender, instance, created, **kwargs):
#     if created:
#         talentnotification = TalentNotification.objects.create(title= f"A New Client {instance.user.fullname} just joined Creve, make your Profile more appealing")
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "talentnotifications",
#             {
#                 'type': 'send_talent_notification',
#                 'notification': {"talent_notification_title":talentnotification.title,
#                                   "talent_notification_date": talentnotification.date.strftime('%Y-%m-%d %H:%M:%S') }
#             }
#         )
    
# def notfi(request):
#     clientnotification = ClientNotification.objects.all()
#     return clientnotification







    

        
    