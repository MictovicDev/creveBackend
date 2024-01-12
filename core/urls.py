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
    path('clientupdate/', views.ClientUpdateView.as_view(), name="clientupdate"),
    path('talentupdate/', views.TalentUpdateView.as_view(), name="talentupdate"),
    path('auth/activation/<str:token>', views.ActivateAccount.as_view(), name='activateaccount'),
]
