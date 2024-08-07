from django.contrib import admin
from django.urls import path,include,re_path
from django.conf import settings
from blog.views import *


urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
    
]