from baseprovider import BaseProvider
import requests
import os

class HundredPayProvider(BaseProvider):
    def verify_payment(self):
        return super().verify_payment()
    
    def send_money(self, headers,payload):
        url = 'https://api.100pay.co/api/v1/pay/charge'
        response = requests.post(url, headers=headers, data=payload)
        return response

    def get_headers(self):
        HundredPay_secret = os.getenv('100PAYPUBLICKEY')
        headers = {
            "Authorization": f"Bearer {HundredPay_secret}",
            "Content-Type": "application/json"
        }
        return headers
