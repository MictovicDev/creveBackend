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
    path('auth/creative/', views.ClientView.as_view(), name='client_signup'),
    path('auth/user/', views.TalentView.as_view(), name='talent_signup'),
    path('auth/activation/<str:token>', views.ActivateAccount.as_view(), name='activateaccount'),
]
