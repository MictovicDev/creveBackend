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
    path('auth/user/', views.ClientView.as_view(), name='client_signup'),
    path('auth/creative/', views.TalentView.as_view(), name='talent_signup'),
    path('auth/user/<str:pk>/', views.ClientUpdateGetDeleteView.as_view(), name="clientupdate"),
    path('auth/userprofile/', views.UserProfileGetView.as_view(), name="usersprofile"),
    path('auth/userprofile/<str:pk>/', views.UserProfileGetUpdateView.as_view(), name="userprofileupdate"),
    path('auth/creativeprofile/', views.CreativeProfileGetView.as_view(), name="creativeprofile"),
    path('auth/creativeprofile/<str:pk>/', views.TalentProfileGetUpdateView.as_view(), name="creativeprofile"),
    path('auth/skill/<str:pk>/', views.SkillGetUpdateView.as_view(), name="create-skill"),
    path('auth/gallery/<str:pk>/', views.GalleryGetUpdateView.as_view(), name="create-gallery"),
    path('auth/question/<str:pk>/', views.QuestionGetUpdateView.as_view(), name="create-question"),
    path('auth/activation/<str:token>', views.ActivateAccount.as_view(), name='activateaccount'),
]
