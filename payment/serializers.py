from core.models import *
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import serializers,response,status
from core.serializers import ClientProfileSerializer, TalentProfileSerializer


class TransactionSerializer(serializers.Serializer):
    client = serializers.CharField()
    creative = serializers.CharField()
    



class BillingSerializer(serializers.Serializer):
    description = serializers.CharField()
    amount = serializers.CharField()
    country = serializers.CharField()
    currency = serializers.CharField()
    # vat = serializers.CharField()
    pricing_type = serializers.CharField()


class CustomerSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()

class MetaData(serializers.Serializer):
    is_approved = serializers.BooleanField()


class HundredPaySerializer(serializers.Serializer):
    transaction = TransactionSerializer()
    ref_id = serializers.CharField()
    customer = CustomerSerializer()
    billing = BillingSerializer()
    metadata = MetaData()
    call_back_url = serializers.CharField()
    # userId = serializers.CharField()
    charge_source = serializers.CharField()

    



    