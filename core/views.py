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
from rest_framework.serializers import ValidationError
from core.models import *
from . import email
from django.dispatch import receiver
import requests
from . import urls
from chat.urls import urlpatterns
from core.serializers import *
from django.db.models.signals import post_save
from .models import TalentProfile
from django.db.models.signals import post_save
import pyotp
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.db.models import Q
from core.serializers import WaitListSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


@receiver(post_save, sender=User)
def post_save_handler(sender, instance, created, **kwargs):
     fullname = instance.fullname
     useremail = instance.email
     otp = instance.otp
     print(otp)
     if created:
       if instance.role == 'Client':
           email.send_linkmail(fullname,useremail,otp)
           ClientProfile.objects.create(user=instance)
       else:
          email.send_linkmail(fullname,useremail,otp)
          TalentProfile.objects.create(user=instance)



class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UpdateOtpSecretView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = OTPSerializer


    def post(self, request, *args, **kwargs):
        # serializer = OTPSerializer(data=request.data)
        try:
            d_email = request.data.get('email')
            try:
                user = User.objects.get(email=d_email)
            except User.DoesNotExist:
                return Response({"message":"User not found"}, status=status.HTTP_404_NOT_FOUND)
            base32secret3232 = pyotp.random_base32()
            otp = pyotp.TOTP(base32secret3232, interval=1000, digits=5)
            time_otp = otp.now()
            otp_secret = base32secret3232
            user.otp = time_otp
            user.otp_secret = otp_secret
            fullname = user.fullname
            d_email = user.email
            user.save()
            email.send_linkmail(fullname,d_email,time_otp)
            return Response({"message":"Token Updated"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Token not updated due to error"})

             
    
    
    


class CreateUserView(generics.ListCreateAPIView):
     serializer_class = UserSerializer
     permission_classes = [permissions.AllowAny]
     queryset = User.objects.all()

     def perform_create(self, serializer):
        if serializer.is_valid():
            base32secret3232 = pyotp.random_base32()
            otp = pyotp.TOTP(base32secret3232, interval=1000, digits=5)
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
        if  pyotp.TOTP(user.otp_secret, interval=1000, digits=5).verify(otp):
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
           


class WaitListView(generics.ListCreateAPIView):
    queryset = Waitlist.objects.all()
    serializer_class = WaitListSerializer
    permission_classes = [permissions.AllowAny]



class ClientUpdateGetDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role='Client')
    lookup_field = 'pk'
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.AllowAny]
    

    def users_update(self, serializer):
        serializer.save()

    def users_destroy(self, instance):
        return super().perform_destroy(instance)
    
class TalentUpdateGetDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.filter(role='Talent')
    lookup_field = 'pk'
    serializer_class = TalentUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    

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
    search_fields = ['category','location','dskills__skill','work_type','digital_skills','nondigital_skills']
    
    
class UnAuthTalentProfileGetView(generics.ListAPIView):
    queryset = TalentProfile.objects.all()
    serializer_class = TalentProfileSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    # search_fields = ['category','location','dskills__skill','work_type','digital_skills','nondigital_skills']



#Used to update the client profile after it has been created by django signals(add the skills and other required attributes)
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
        instance = serializer.save()

    # def perform_update(self,serializer):
    #     try:
    #         pk = self.kwargs.get('pk')
    #         serializer.save()
    #         print(dir(serializer))
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except ValidationError as e:
    #         error_data = {'error': str(e)}
    #         raise ValidationError(error_data)
        




class ListReview(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        try:
            try:
                talent_profile = TalentProfile.objects.get(user=self.request.user)
                bookies = Review.objects.filter(reviewed=talent_profile)
            except TalentProfile.DoesNotExist:
                client_profile = ClientProfile.objects.get(user=self.request.user)
                bookies = Review.objects.filter(reviewer=client_profile)
            return bookies
        except Review.DoesNotExist:
            return []


    
class ReviewCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        try:
            client_profile = ClientProfile.objects.get(user=self.request.user)
            print(client_profile)
            talent_profile = TalentProfile.objects.get(id=pk)
            bookies = Review.objects.filter(reviewed=talent_profile,  reviewer=client_profile)
            return bookies
        except Review.DoesNotExist:
            return []
        
    

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        if serializer.is_valid():
            print('Yes')
            content = serializer.validated_data['content']
            rating = serializer.validated_data['rating']
            try:
                client_profile = ClientProfile.objects.get(user=self.request.user)
                print(client_profile)
            except ClientProfile.DoesNotExist:
                print('Yes from client')
                data = {"message": "Client not found"}
                return  Response(data=data, status=status.HTTP_404_NOT_FOUND)
            try:
                talent_profile = TalentProfile.objects.get(id=pk)
                print(talent_profile)
            except TalentProfile.DoesNotExist:
                data = {"message": "Client not found"}
                return  Response(data=data, status=status.HTTP_404_NOT_FOUND)
            if talent_profile and client_profile:
                try:
                    review = Review.objects.create(
                        content=content,
                        rating = rating,
                        reviewer=client_profile,
                        reviewed=talent_profile
                    )
                    print('Review created successfully')
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    print(f'Error creating Review: {e}')
                    return Response({"message": "Failed to create review"}, status=status.HTTP_400_BAD_REQUEST)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


            
class BookView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookedCreative.objects.all()
    serializer_class = BookedCreativeSerializer

    def get_queryset(self):
        try:
            try:
                talent_profile = TalentProfile.objects.get(user=self.request.user)
                bookies = BookedCreative.objects.filter(talent_profile=talent_profile)
            except TalentProfile.DoesNotExist:
                print("YEs")
                client_profile = ClientProfile.objects.get(user=self.request.user)
                print(client_profile)
                bookies = BookedCreative.objects.filter(client_profile=client_profile)
            return bookies
        except BookedCreative.DoesNotExist:
            return []


class BookCreativeView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookedCreative.objects.all()
    serializer_class = BookedCreativeSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        try:
            client_profile = ClientProfile.objects.get(user=self.request.user)
            print(client_profile)
            talent_profile = TalentProfile.objects.get(id=pk)
            bookies = BookedCreative.objects.filter(talent_profile=talent_profile, client_profile=client_profile)
            return bookies
        except BookedCreative.DoesNotExist:
            return []


    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        print(pk)
        if serializer.is_valid():
            print('Yes')
            title = serializer.validated_data['title']
            description = serializer.validated_data['description']
            phone_number = serializer.validated_data['phone']
            try:
                client_profile = ClientProfile.objects.get(user=self.request.user)
            except ClientProfile.DoesNotExist:
                print('Yes from client')
                data = {"message": "Client not found"}
                return  Response(data=data, status=status.HTTP_404_NOT_FOUND)
            try:
                talent_profile = TalentProfile.objects.get(id=pk)
                talent_email = talent_profile.user.email
                print(talent_profile.user.email)
            except TalentProfile.DoesNotExist:
                data = {"message": "Client not found"}
                return  Response(data=data, status=status.HTTP_404_NOT_FOUND)
            if talent_profile and client_profile:
                BookedCreative.objects.create(talent_profile=talent_profile, client_profile=client_profile, title=title, description=description, phone=phone_number)
                print(client_profile.user.fullname)
                email.send_booking_mail(fullname=talent_profile.user.fullname, clientname=client_profile.user.fullname, useremail=talent_email)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"message": "Users not found"}, status= status.HTTP_404_NOT_FOUND)
        else:
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            


class SkillsListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SkillSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            profile = TalentProfile.objects.get(user=user)
            return Skill.objects.filter(talentprofile=profile)
        except TalentProfile.DoesNotExist:
            return Skill.objects.none()

        
    def perform_create(self, serializer):
        if serializer.is_valid():
            if self.request.user.is_authenticated:
                    try:
                        user = self.request.user
                        talentprofile = TalentProfile.objects.get(user=user)
                        skills_data = serializer.validated_data.get('skills_list', [])
                        print(skills_data)
                        if skills_data:
                            Skill.objects.bulk_create([
                                Skill(talentprofile=talentprofile, skill=skill_data)
                                for skill_data in skills_data
                            ])
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except TalentProfile.DoesNotExist:
                        return Response({"message":"TalentProfile Does not exist"})
            return Response({"message": "you must be logged in to create question"})
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    


class GalleryListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GallerySerializer

    def get_queryset(self):
        
        user = self.request.user
        try:
            profile = TalentProfile.objects.get(user=user)
            return Gallery.objects.filter(talentprofile=profile)
        except TalentProfile.DoesNotExist:
            return Gallery.objects.none()

        
    def perform_create(self, serializer):
        if serializer.is_valid():
            if self.request.user.is_authenticated:
                    try:
                        user = self.request.user
                        talentprofile = TalentProfile.objects.get(user=user)
                        gallery_data = serializer.validated_data.get('images_list', [])
                        if gallery_data:
                            Gallery.objects.bulk_create([
                                Gallery(talentprofile=talentprofile, image=image)
                                for image in gallery_data
                            ])
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except TalentProfile.DoesNotExist:
                        return Response({"message":"TalentProfile Does not exist"})
            return Response({"message": "you must be logged in to create question"})
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    


class VerifyUserView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NinSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            profile = TalentProfile.objects.get(user=user)
            return Nin.objects.filter(talentprofile=profile)
        except TalentProfile.DoesNotExist:
            return Nin.objects.none()
        
    def perform_create(self, serializer):
        if serializer.is_valid():
            image = serializer.validated_data['image']
            try:
                user = self.request.user
                talentprofile = TalentProfile.objects.get(user=user)
            except TalentProfile.DoesNotExist:
                raise ValidationError({"Message": "Talent Profile Does not exist"})
            if Nin.objects.filter(talentprofile=talentprofile).exists():
                    print('True')
                    raise ValidationError({"Message": "You can only upload your NIN once."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(talentprofile=talentprofile, image=image)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    

class SkillUpdateDel(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'pk'


    
    def skill_update(self, serializer):
        instance = serializer.save()
        return instance

    def skill_destroy(self, instance):
        return super().perform_destroy(instance)
                
        

class GalleryUpdateDel(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    lookup_field = 'pk'


    
    def gallery_update(self, serializer):
        instance = serializer.save()
        return instance

    def gallery_destroy(self, instance):
        return super().perform_destroy(instance)



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
    # queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # print(dir(generics.ListAPIView))

    def get_queryset(self):
        user = self.request.user
        try:
            profile = TalentProfile.objects.get(user=user)
            return Question.objects.filter(talent_profile=profile)
        except TalentProfile.DoesNotExist:
            return Question.objects.none()

        
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
            

            
class DocumentApi(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        data = {}
        for item in urls.urlpatterns:
            name = ' '.join(item.name.split('_'))
            data[name.capitalize()] = str(item.pattern)
        for item in urlpatterns:
            name = ' '.join(item.name.split('_'))
            data[name.capitalize()] = str(item.pattern)
        return Response(data=data, status=status.HTTP_200_OK)
    

# 1. Get Total Number of Creatives ( and all creatives) Done
# 2. Get Total Number of Clients (and all clients) Done
# 3. Get Total Number of Request Done
# 4. Get Active Users per week
# 6. Get Complains 
# 6. Delete account Done
# 7. Verify Creative Done
# 8. Ban Creative 
# 9. Unban Creative
    
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_creatives(self):
    creatives = {
        
    }
    return Response(creatives, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_app_info(self):
    info = {
        'no_clients':  len(ClientProfile.objects.all()),
        'no_creatives':  len(TalentProfile.objects.all()),
        'no_requests':  len(BookedCreative.objects.all()),
    }
    return Response(info, status=status.HTTP_200_OK)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated, IsAdminUser])
# def get_all_requests(self):
#     try:
#         requests = {
#     }
#         return Response(requests, status=status.HTTP_200_OK)
#     except BookedCreative.DoesNotExist():
#         return Response({"message": "Can't get the Numbers of Request Right Now"}, status= status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def filtered_talents(request, pk):
    try:
        talent = TalentProfile.objects.get(id=pk)
        print(talent.digital_skills)
        if talent.digital_skills == '':
            skills = talent.nondigital_skills
        else:
            skills = talent.digital_skills
        profession = talent.display_name
        all_talent = TalentProfile.objects.filter(
             Q(digital_skills= skills) |
            (Q(display_name=profession))).exclude(id=pk)
        serializer = TalentProfileSerializer(all_talent, many=True,context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    except TalentProfile.DoesNotExist:
        return Response({"message": "talentprofile does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, pk):
    try:
        model_instance = User.objects.get(id=pk)
        print(model_instance)
        model_instance.delete()
        return Response({"message": "Model deleted successfully"})
    except User.DoesNotExist:
        return Response({"error": "Model not found"}, status=status.HTTP_404_NOT_FOUND)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def verify_creative(request, pk):
    talent = TalentProfile.objects.get(id=pk)
    Verification.objects.create(profile=talent, verified=True)
    return Response({"message": "TalentProfile has been Verified"})



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def ban_user(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = False
    user.save()
    return Response({"message":"User has been Banned"}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def unban_user(request,pk):
    user = User.objects.get(id=pk)
    user.is_active = True
    user.save()
    return Response({"message":"User has been unBanned"}, status=200)





    
    











    

        
    