from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import HundredPaySerializer
import json
from .provider.provider_factory import ProviderFactory
from .models import Transaction


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def hundred_pay(request, pk=''):
    transaction_type= '100Pay'
    if request.method == 'POST':
        serializer = HundredPaySerializer(data=request.data)
        if serializer.is_valid():
            json_data = json.dumps(serializer.data)
            print(json_data)
            provider = ProviderFactory.createprovider(transaction_type)
            headers = provider.get_headers()
            print(headers)
            response = provider.create_payment_charge(headers,payload=json_data)
            if response.status_code == '200':
                Transaction.objects.create(client=client, creative=creative)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=400)
    
    elif request.method == 'GET':
        id = pk
        provider = ProviderFactory.createprovider(transaction_type)
        headers = provider.get_headers()
        response = provider.get_payment_charge(headers, id)
        return Response(response.json(), status=response.status_code)