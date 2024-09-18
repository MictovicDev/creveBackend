from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from django.conf.urls.static import static
from payment.views import *


urlpatterns = [
   path('', hundred_pay, name='create_transaction'),
]