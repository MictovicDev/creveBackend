from core.models import *
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import serializers,response,status


# class HundredPaySerializer(serializers.ModelSerializer):

#     class Meta:
#         fields = ['']

# "customer": {
#     "user_id": "111",
#     "name": "Brainy Josh",
#     "phone": "80123456789",
#     "email": "user@site.com"
# },

# "billing": {
#     "description": "MY TEST PAYMENT",
#     "amount": "10000",
#     "country": "NG",
#     "currency": "NGN",
#     "vat": "10",
#     "pricing_type": "fixed_or_partial_price"
# },

class BillingSerializer(serializers.Serializer):
    description = serializers.CharField()
    amount = serializers.CharField()
    country = serializers.CharField()
    currency = serializers.CharField()
    vat = serializers.CharField()
    pricing_type = serializers.CharField()


class CustomerSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    BillingSerializer()
    call_back_url = serializers.CharField()
    userId : "6143bfb7fe85e0020bf243f9",
"charge_source": "api"

    