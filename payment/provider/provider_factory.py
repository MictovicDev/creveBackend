from  .HundredPay import HundredPayProvider
# from .airvend import AirVendProvider
# from .paystack import PayStackProvider
import json

class ProviderFactory:
    """Used to Create Different Providers in Runtime"""
    @staticmethod
    def createprovider(type):
        # data = json.loads(payload)
        if type == '100Pay':
            return HundredPayProvider()
        # if type == 'FUND':
        #     return PayStackProvider()