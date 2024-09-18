from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import HundredPaySerializer, TransactionSerializer
import json
from .provider.provider_factory import ProviderFactory
from .models import Transaction
from core.models import TalentProfile, ClientProfile


# @api_view(['POST'])
# @permission_classes([IsAuthenticated, IsAdminUser])
# def hundred_pay(request):
#     transaction_type= '100Pay'
#     if request.method == 'POST':
#         serializer = HundredPaySerializer(data=request.data)
#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             transaction = validated_data.pop('transaction', None)  # Pop 'transaction' from validated_data
#             creative_id = transaction.get('creative')
#             client_id = transaction.get('client')
#             json_data = json.dumps(validated_data)
#             print(json_data)
#             provider = ProviderFactory.createprovider(transaction_type)
#             headers = provider.get_headers()
#             print(headers)
#             response = provider.create_payment_charge(headers,payload=json_data)
#             if response.status_code == 200:
#                 client = ClientProfile.objects.get(id=client_id)
#                 creative = TalentProfile.objects.get(id=creative_id)
#                 chargeId = response.json().get('chargeId')
#                 Transaction.objects.create(client=client, creative=creative, charge_id=chargeId)
#                 return Response(response.json(), status=response.status_code)
#         return Response(serializer.errors, status=400)
    

       

# @api_view(['GET'])
# @permission_classes([IsAuthenticated, IsAdminUser])
# def get_payment_charge(request, pk):
#     transaction_type= '100Pay'
#     id = pk
#     provider = ProviderFactory.createprovider(transaction_type)
#     headers = provider.get_headers()
#     response = provider.get_payment_charge(headers, id)
#     print(response)
#     return Response(response.json(), status=response.status_code)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def hundred_pay(request):
    serializer = TransactionSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data
        client_id = validated_data.get('client', None)
        creative_id = validated_data.get('creative', None)
        client = ClientProfile.objects.get(id=client_id)
        creative = TalentProfile.objects.get(id=creative_id)
        Transaction.objects.create(client=client, creative=creative)
        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)