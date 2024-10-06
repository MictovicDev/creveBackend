from django.shortcuts import render
from django.shortcuts import render, redirect
from rest_framework import generics,permissions, response, status,filters
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from core.serializers import MyTokenObtainPairSerializer, UserSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from django.dispatch import receiver
import requests
from . import urls
import json
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
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
import os
from core.models import TalentProfile
from .models import Payment, Wallet, SolPayment
from .serializers import  SolPaymentSerialzer

# Create your views here.



# {"retries":0,"acknowledged":false,"dispatched":false,"type":"credit","_id":"66deb5e0a7044f0049e24ca3","chargeId":"66deb58ea7044f0049e24c69","reference":"lEdWUHVGoCnUMYG9","data":{"from":"0x8ad4BFe54f00C6B7A394a21405a12bfdd3f97851","to":"160005","network":"bsc","transaction_id":"internal-transfer-66deb5dfa7044f0049e24c96","status":"CONFIRMED","timestamp":"2024-09-09T08:46:24.057Z","value":{"local":{"amount":"242.95","currency":"NGN"},"crypto":{"amount":5,"currency":"PAY"}},"block":{"hash":"internal-transfer-66deb5dfa7044f0049e24c96"},"charge":{"customer":{"user_id":"1","name":"Express User","email":"joshuabrendan5@gmail.com","phone":"0000000000"},"billing":{"currency":"PAY","vat":0,"pricing_type":"fixed_price","amount":"5","description":"test","country":"US"},"status":{"context":{"status":"overpaid","value":142.95},"value":"overpaid","total_paid":242.95},"ref_id":"fb324f73-8733-47e2-b371-8a766235694d","payments":[{"from":"0x8ad4BFe54f00C6B7A394a21405a12bfdd3f97851","to":"160005","network":"bsc","transaction_id":"internal-transfer-66deb5dfa7044f0049e24c96","status":"CONFIRMED","timestamp":"2024-09-09T08:46:24.057Z","value":{"local":{"amount":"242.95","currency":"NGN"},"crypto":{"amount":5,"currency":"PAY"}},"block":{"height":null,"hash":"internal-transfer-66deb5dfa7044f0049e24c96"}}],"charge_source":"external","createdAt":"2024-09-07T12:05:46.431Z","_id":"66deb58ea7044f0049e24c69","metadata":{"is_approved":"yes","order_id":"OR2","charge_ref":"REF"},"call_back_url":"http://localhost:8000/verifyorder/","app_id":"64971290f6dbaf011f729325","userId":"64970fbdf6dbaf011f7292be","chargeId":"66deb58ea7044f0049e24c69","__v":0},"appId":"64971290f6dbaf011f729325"},"cryptoChargeId":"66deb593a7044f0049e24c73","createdAt":"2024-09-09T08:46:24.477Z","__v":0}

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_payment(request):
    api_secret = os.getenv('API_SECRET')
    received_token = request.META.get('HTTP_VERIFICATION_TOKEN')
    if received_token == api_secret:
        payload = json.loads(request.body.decode('utf-8'))
        charge_id = payload.get('chargeId')
        # print(charge_id)
        data = payload.get('data')
        charge = data.get('charge')
        talent_id = charge.get('metadata').get('talent_id')
        transaction_id = data.get('transaction_id')
        network = data.get('network')
        status = data.get('status')
        timestamp = data.get('timestamp')
        value = data.get('value')
        amount = charge.get('billing').get('amount')
        print(amount)
        client_id = charge.get('metadata').get('client_id')
        try:
            talent = TalentProfile.objects.get(user__id=talent_id)
        except TalentProfile.DoesNotExist:
             return Response({"message": "Talent profile does not exist"}, status=404)
        try:
            client = ClientProfile.objects.get(user__id=client_id)
        except ClientProfile.DoesNotExist:
             return Response({"message": "Client profile does not exist"}, status=404)
        print(talent, client)
        payment, created = Payment.objects.get_or_create(
                transaction_id=transaction_id,
                defaults={
                    'network': network,
                    'status': status,
                    'timestamp': timestamp,
                    'value': value,
                    'client_id': client,
                    'talent_id': talent
                }
            )
        if created:
            print('Payment created successfully.')
            headers = {
                'api-key': os.getenv('API_SECRET'),
                'Content-Type': 'application/json' 
            }
            
            # Make a request to another endpoint
            external_endpoint = f"https://api.100pay.co/api/v1/pay/crypto/payment/{charge_id}"  # Replace with your endpoint
            response = requests.post(
                external_endpoint, headers=headers)
            
            if response.status_code == 200:
                print(f"Response Headers: {response.headers}")
                print('Successfully notified external endpoint.')
                withdrawable_balance = 0.03 * amount
                Wallet.objects.create(earnings=amount, withdrawable_balance=withdrawable_balance, owner=talent)
            else:
                print(f'Failed to notify external endpoint: {response.content}')

        else:
                print('Payment already exists.')
        return Response(payload)
    return Response("Error")

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createsolpayment(request):
    client_id = request.POST.get('client_id')
    talent_id = request.POST.get('talent_id')
    amount = request.POST.get('amount')
    # print(type(amount))
    print(client_id, talent_id, amount)
    description = request.POST.get('description')
    try:
        client = ClientProfile.objects.get(id=client_id)
    except ClientProfile.DoesNotExist:
        return Response({"message":"Client Profile Matching Query Does not Exists"}, status=404)
    try:
         talent = TalentProfile.objects.get(id=talent_id)
    except TalentProfile.DoesNotExist:
        return Response({"message":"Talent Profile Matching Query Does not Exists"}, status=404)
    solpayment = SolPayment.objects.create(client=client, talent=talent, amount=amount, description=description)
    wallet, created = Wallet.objects.get_or_create(owner=talent)
    wallet.earnings += int(amount)
    wallet.save()
    serializer = SolPaymentSerialzer(solpayment)
    return Response(serializer.data, status=200)
     
    

