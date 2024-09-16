from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from payment.views import *


urlpatterns = [
   path('', hundred_pay, name='create_payment_charge'),
   path('<str:pk>/', hundred_pay, name='get_payment_charge')
]