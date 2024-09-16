from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import HundredPaySerializer
import json
from .providers.provider_factory import ProviderFactory


# Create your views here.
# class HundredPayView(generics.CreateAPIView):
#     serializer_class = HundredPaySerializer
#     transaction_type = 'hundredpay'
#     permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def hundred_pay(request):
    transaction_type= '100pay'
    serializer = HundredPaySerializer(data=request.data)
    if serializer.is_valid():
        json_data = json.dumps(serializer.data)
        provider = ProviderFactory.createprovider(transaction_type)
        headers = provider.get_headers()
        response = provider.send_money(headers,payload=json_data)
        return Response(response.json(), status=response.status_code)

    return Response(response.json(), status=response.status_code)