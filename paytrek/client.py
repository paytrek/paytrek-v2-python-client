import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Paytrek(object):
    BASE_URLS = {
        'sandbox': 'https://sandbox.paytrek.com',
        'worldwide_live': 'https://secure.paytrek.com',
        'turkey_live': 'https://secure.paytrek.com.tr'
    }

    def __init__(self, username, password, environment='sandbox'):
        self.basic_auth = (username, password)
        self.base_url = self.BASE_URLS.get(environment)
        self.endpoints = {
            'sale': ''.join([self.base_url, '/api/v2/sale/']),
            'charge': ''.join([self.base_url, '/api/v2/charge/']),
            'direct_charge': ''.join([self.base_url, '/api/v2/direct_charge/']),
            'capture': ''.join([self.base_url, '/api/v2/capture/']),
            'refund': ''.join([self.base_url, '/api/v2/refund/']),
            'charge_with_token': ''.join([self.base_url, '/api/v2/charge_with_token/']),
            'vault': ''.join([self.base_url, '/api/v2/vault/']),
        }
        self.headers = {'Content-type': 'application/json'}

    def _request(self, url, query={}):
        """
        Returns json response according to defined endpoint

        :param url:
        :param query:
        :return:
        """
        response = requests.post(url=url, auth=self.basic_auth, json=query,
                                 headers=self.headers, verify=False)
        if not response.ok:
            raise Exception(response.text)
        return response.json()

    def sale(self, payload=None, sale_token=None):
        """
        Returns json response within sale result
        to create sale resource payload is required
        to get created sale resource sale_token is required

        :param payload: https://paytrek.docs.apiary.io/#reference/0/sale/create-sale
        :param sale_token:
        :return:
        """
        if payload:
            response = requests.post(url=self.endpoints.get('sale'),
                                     json=payload, headers=self.headers,
                                     auth=self.basic_auth, verify=False)
        elif sale_token:
            url = ''.join([self.endpoints.get('sale'), sale_token, '/'])
            response = requests.get(url=url, headers=self.headers,
                                    auth=self.basic_auth, verify=False)
        if not response.ok:
            raise Exception(response.text)
        return response.json()

    def charge(self, payload):
        """
        Returns json response within charge result

        :param payload: https://paytrek.docs.apiary.io/#reference/0/charge/charge-sale
        :return:
        """
        return self._request(self.endpoints.get('charge'), query=payload)

    def direct_charge(self, payload):
        """
        Returns json response within direct charge result

        :param payload: https://paytrek.docs.apiary.io/#reference/0/direct-charge/charge-sale
        :return:
        """
        return self._request(self.endpoints.get('charge'), query=payload)

    def charge_with_token(self, sale_token, card_token):
        """
        Returns json response within succeeded or failed result

        :param sale_token:
        :param card_token:
        :return:
        """
        payload = {
            'sale': '{}'.format(sale_token),
            'card_token': card_token,
        }
        return self._request(self.endpoints.get('charge_with_token'), query=payload)

    def capture(self, sale_token, comments=None):
        """
        Returns json response within succeeded or fail result

        :param comments: comments for accepting the fraud review decision
        :param sale_token:
        :return:
        """
        params = {'comments': comments}
        url = ''.join([self.endpoints.get('capture'), sale_token, '/'])
        return self._request(url, query=params)

    def cancel(self, sale_token, comments=None):
        """
        Returns json response within cancel or fail result

        :param sale_token:
        :param comments: comments for reject decision
        :return:
        """
        params = {
            'comments': comments
        }
        url = ''.join([self.endpoints.get('cancel'), sale_token, '/'])
        return self._request(url, query=params)

    def refund(self, sale_token, amount=None, comments=None):
        """
        Returns json response within refund or fail result

        :param sale_token:
        :param amount: amount to refund
        :param comments: comments for reject decision
        :return:
        """
        params = {
            'amount': amount,
            'comments': comments
        }
        url = ''.join([self.endpoints.get('refund'), sale_token, '/'])
        return self._request(url, query=params)

    def vault(self, payload):
        """
        Returns json response representing payment token and strict card information
        such as bin number, bin country, card currency and card issuer.

        :param payload: https://paytrek.docs.apiary.io/#reference/0/vault/vault-card
        :return:
        """
        return self._request(self.endpoints.get('vault'), query=payload)
