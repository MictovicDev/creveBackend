from django.urls import path,include
from . import views


urlpatterns = [
    path('verify-payment-hook/', views.verify_payment, name='verify-payment'),
    path('sol-payment/', views.createsolpayment, name='createsolpayment'),
    # path('withdraw', views.withdraw, name='allchats'),
    # path('createpin', views.createpin, name='createpin')
]