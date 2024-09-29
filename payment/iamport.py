import json
import requests

IAMPORT_API_URL = 'https://api.iamport.kr/'

class Iamport(object):
    def __init__(self, imp_key, imp_secret, imp_url=IAMPORT_API_URL):
        self.imp_key = imp_key
        self.imp_secret = imp_secret
        self.imp_url = imp_url
        requests_session = requests.Session()
        requests_adapters = requests.adapters.HTTPAdapter(max_retries=3)
        requests_session.mount('https://', requests_adapters)
        self.requests_session = requests_session

    class ResponseError(Exception):
        def __init__(self, code=None, message=None):
            self.code = code
            self.message = message

    class HttpError(Exception):
        def __init__(self, code=None, reason=None):
            self.code = code
            self.reason = reason

    @staticmethod
    def get_response(response):
        if response.status_code != requests.codes.ok:
            raise Iamport.HttpError(response.status_code, response.reason)
        result = response.json()
        if result['code'] != 0:
            raise Iamport.ResponseError(result.get('code'), result.get('message'))
        return result.get('response')

    def _get_token(self):
        url = f"{self.imp_url}users/getToken"
        payload = {
            'imp_key': self.imp_key,
            'imp_secret': self.imp_secret
        }
        response = self.requests_session.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(payload))
        return self.get_response(response).get('access_token')

    def get_headers(self):
        return {'Authorization': self._get_token()}

    def _get(self, url, payload=None):
        headers = self.get_headers()
        response = self.requests_session.get(url, headers=headers, params=payload)
        return self.get_response(response)

    def find_by_imp_uid(self, imp_uid):
        """ imp_uid를 통해 결제 조회 """
        url = f"{self.imp_url}payments/{imp_uid}"
        return self._get(url)

    def find_by_merchant_uid(self, merchant_uid):
        """ merchant_uid를 통해 결제 조회 """
        url = f"{self.imp_url}payments/find/{merchant_uid}"
        return self._get(url)

    def cancel_payment(self, imp_uid=None, merchant_uid=None, reason=None, amount=None):
        """ 결제 취소 요청 """
        url = f"{self.imp_url}payments/cancel"
        payload = {
            'reason': reason,
        }
        if imp_uid:
            payload['imp_uid'] = imp_uid
        if merchant_uid:
            payload['merchant_uid'] = merchant_uid
        if amount:
            payload['amount'] = amount
        
        return self.requests_session.post(url, headers=self.get_headers(), data=json.dumps(payload)).json()
