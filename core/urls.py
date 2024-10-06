from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'), #you can use to login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api', views.DocumentApi.as_view(), name="endpoints" ),
    path('auth/', views.CreateUserView.as_view(), name='client_signup'),
    # path('auth/creative/', views.TalentView.as_view(), name='talent_signup'),
    path('auth/activation/', views.ActivateAccount.as_view(), name='activateaccount'),
    path('questions/', views.QuestionListCreateView.as_view(), name='question-create'),
    path('questions/<str:pk>/', views.QuestionUpdateDel.as_view(), name='question-list'),
    path('userprofile/', views.ClientProfileGetView.as_view(), name="usersprofile"),
    path('user/<str:pk>/', views.ClientUpdateGetDeleteView.as_view(), name="clientupdate"),
    path('userprofile/<str:pk>/', views.ClientProfileGetUpdateView.as_view(), name="userprofileupdate"),
    path('creativeprofile/', views.TalentProfileGetView.as_view(), name="creativeprofile"),
    path('tcreativeprofile/', views.UnAuthTalentProfileGetView.as_view(), name="tcreativeprofile"),
    path('creativeprofile/<str:pk>/', views.TalentProfileGetUpdateView.as_view(), name="creativeprofile"),
    path('skills/', views.SkillsListCreateView.as_view(), name="create-skill"),
    path('skills/<str:pk>/', views.SkillUpdateDel.as_view(), name='skillupdate'),
    path('nins/', views.VerifyUserView.as_view(), name='nin_verification'),
    path('reviews/<str:pk>/', views.ReviewCreateView.as_view(), name="create_review"),
    path('bookcreatives/<str:pk>/', views.BookCreativeView.as_view(), name="book_creative"),
    path('approve-request/<str:pk>/', views.BookCreativeUpdateView.as_view(), name="approve"),
    path('books/', views.BookView.as_view(), name="books"),
    path('reviews/', views.ListReview.as_view(), name='reviews'),
    path('waitlist/', views.WaitListView.as_view(), name='waitlist'),
    path('gallery/', views.GalleryListCreateView.as_view(), name="create-gallery"),
    path('gallery/<str:pk>/', views.GalleryUpdateDel.as_view(), name= "delete-gallery"),
    path('otp/', views.UpdateOtpSecretView.as_view(), name='otp'),
    ##Admin Dashboard
    path('info/', views.get_app_info, name='info'),
    path('creatives/', views.get_creatives, name='creatives'),
    path('removeuser/<str:pk>/', views.delete_user, name='delete_user'),
    path('verify/<str:pk>/', views.verify_creative, name="verify_creative"),
    path('ban/<str:pk>/', views.ban_user, name='ban_user'),
    path('unban/<str:pk>/', views.unban_user, name='unban_user'),
    ##end of admin dashboard
    path('talents/<str:pk>/', views.filtered_talents, name='filtered_talents'),
]
