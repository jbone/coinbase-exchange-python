#
# CoinbaseExchange/Coinbase.py
# Daniel Paquin
#
# The wrapper class Coinbase() communcates with the Coinbase Exchange API
# time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from CBEOrderDO import CBEOrderDO
from CandlestickDO import CandlestickDO
from pprint import pprint

################
### API Keys ###
################

base_url = "https://api.exchange.coinbase.com/"
# TODO: Make this more secure and grab from file.
_key = "key"
_secret = "secret"
_passphrase = "passphrase"

class Coinbase():

    ###################
    ### Market Data ###
    ###################
    # Public Endpoints

    def getOrderBook(self):

        response = requests.get(base_url + 'products/BTC-USD/book?level=2')
        
        return response.json()

    def getProducts(self):

        response = requests.get(base_url + 'products')

        return response.json()

    def getDayStats(self):

        response = requests.get(base_url + 'products/BTC-USD/stats')
        
        return response.json()

    def getServerTime(self):

        response = requests.get(base_url + 'time')
        
        return response.json()

    def getCandlesticks(self, startTime='', endTime='', granularity=''):

        payload = {
            "start" : startTime,
            "end" : endTime,
            "granularity" : granularity # in seconds
        }

        response = requests.get(base_url + 'products/BTC-USD/candles', params=payload)
        pprint(response.json())

        if 'message' in response.json():
            print "\nERROR:", response.json()['message']
            return 0

        return response.json()

    ###############
    ### Account ###
    ###############
    # Private Endpoints

    def getAccounts(self, accountId = ""):
        payload = getAuth(_key, _secret, _passphrase)

        r = requests.get(base_url + 'accounts/' + accountId, auth=payload)
        
        return r.json()

    ##############
    ### Orders ###
    ##############
    # Private Endpoints

    def getOrders(self, CBEOrderDO):
        payload = getAuth(_key, _secret, _passphrase)

        if CBEOrderDO.orderId is not None:
            r = requests.get(base_url + 'orders/' + CBEOrderDO.orderId, auth=payload)
        else:
            r = requests.get(base_url + 'orders', auth=payload)
        
        return r.json()

    def getFills(self, CBEOrderDO):
        payload = getAuth(_key, _secret, _passphrase)

        # Get Fills for a specific order
        if CBEOrderDO.orderId is not None:
            payload.update({
                'order_id' : CBEOrderDO.orderId
            })
            r = requests.get(base_url + 'fills', auth=payload)
        
        # Get Fills for a specific product
        elif CBEOrderDO.product_id is not None:
            payload.update({
                'product_id' : CBEOrderDO.product_id
            })
            r = requests.get(base_url + 'fills', auth=payload)
        
        # Get all Fills
        else:
            r = requests.get(base_url + 'fills', auth=payload)
        
        return r.json()

    def placeOrder(self, CBEOrderDO):
        payload = getAuth(_key, _secret, _passphrase)
        
        payload.update({
            'type' : CBEOrderDO.order_type,
            'side' : CBEOrderDO.side,
            'product_id' : CBEOrderDO.product,
            'stp' : CBEOrderDO.stp,
            'price' : CBEOrderDO.size,
            'size' : CBEOrderDO.size,
            'time_in_force' : CBEOrderDO.time_in_force,
            'cancel_after' : CBEOrderDO.cancel_after
            })

        r = requests.post(base_url + 'orders', auth=payload)
        
        return r.json()

    def cancelOrders(self, CBEOrderDO):
        payload = getAuth(_key, _secret, _passphrase)

        if CBEOrderDO.orderId is not None:
            r = requests.delete(base_url + 'orders/' + CBEOrderDO.orderId, auth=payload)
        else:
            r = requests.delete(base_url + 'orders', auth=payload)

        return r.json()


######################
### Authentication ###
######################
# Provided by Coinbase

class getAuth(AuthBase):

    def __init__(self, api_key, secret_key, passphrase):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')
        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
        })

        return request