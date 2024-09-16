from .baseprovider import BaseProvider
import requests
import os

class HundredPayProvider(BaseProvider):
    def verify_payment(self):
        return super().verify_payment()
    
    def create_payment_charge(self, headers,payload):
        url = 'https://api.100pay.co/api/v1/pay/charge'
        response = requests.post(url, headers=headers, data=payload)
        return response
    
    def get_payment_charge(self, headers, id):
        url = f'https://api.100pay.co/api/v1/pay/charge/{id}'
        response = requests.get(url, headers=headers)
        return response

    def get_headers(self):
        HundredPay_secret = os.getenv('100PAYPUBLICKEY')
        headers = {
            'api-key': HundredPay_secret,
            "Content-Type": "application/json"
        }
        return headers
    
