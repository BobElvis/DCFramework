import os
from dotenv import load_dotenv
from UrlHeaderGenerator import UrlHeaderGenerator
from aws_signing import AwsSigningV4
import requests


load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
api_key = os.environ.get("API_KEY")


class Person:
    def __init__(self, ssn):
        # Create API objects
        api_token_params = {"customerId": '{"type":"SSN", "value":"%s"}' % ssn}
        api_token_path = "/token"
        self.aws_signing_v4 = AwsSigningV4(
            aws_access_key_id=client_id,
            aws_secret_access_key=client_secret,
            aws_host="developer-api-sandbox.dnb.no",
            aws_region="eu-west-1",
            aws_service="execute-api",
        )
        self.url_header_generator = UrlHeaderGenerator(
            endpoint="https://developer-api-sandbox.dnb.no",
            aws_signing_v4=self.aws_signing_v4,
        )
        # Get user token
        api_token_response = self.get_token(api_token_path, api_token_params)
        self.api_token = api_token_response.json()["tokenInfo"][0]["jwtToken"]

    def get_token(self, api_token_path, api_token_params):
        request_url, headers = self.url_header_generator.generate(
            path=api_token_path, params=api_token_params, api_key=api_key, method="GET"
        )

        return requests.get(request_url, headers=headers)

    def get(self, path, params):
        request_url, headers = self.url_header_generator.generate(
            path=path, params=params, api_token=self.api_token, api_key=api_key, method="GET"
        )
        return requests.get(request_url, headers=headers)

    def put(self, path, params):
        request_url, headers = self.url_header_generator.generate(
            path=path, params=params, api_token=self.api_token, api_key=api_key, method="PUT"
        )
        return requests.put(request_url, headers=headers)

    def post(self, path, params, data):
        request_url, headers = self.url_header_generator.generate(
            path=path, params=params, api_token=self.api_token, api_key=api_key, method="POST"
        )
        return requests.post(request_url, data=data, headers=headers)

    def delete(self, path, params):
        request_url, headers = self.url_header_generator.generate(
            path=path, params=params, api_token=self.api_token, api_key=api_key, method="POST"
        )
        return requests.delete(request_url, headers=headers)

    def get_accounts(self):
        return self.get("/accounts/", {})

    def get_account_details(self, account_number: str):
        return self.get("/accounts/" + account_number, {})

    def get_account_balance(self, account_number: str):
        return self.get("/accounts/" + account_number + "/balance", {})

    def get_cards(self):
        return self.get("/cards/", {})

    def get_card_details(self, card_id: str):
        return self.get("/cards/" + card_id, {})

    def get_card_balance(self, card_id: str):
        return self.get("/cards/" + card_id + "/balance", {})

    def get_customer_details(self):
        return self.get("/customers/current", {})

    def get_due_payments(self, account_number: str):
        return self.get("/payments/" + account_number + "/due", {})

    def get_due_payments_by_id(self, account_number: str, payment_id: str):
        return self.get("/payments/" + account_number + "/due/" + payment_id, {})

    def get_transactions(self, account_number: str):
        return self.get("/transactions/" + account_number + "/", {})

    def put_block_card(self, card_id):
        return self.put("/cards/" + card_id + "/block", {})

    def put_unblock_card(self, card_id):
        return self.put("/cards/" + card_id + "/unblock", {})

    # NOT WORKING? However APIs are static sooooooo...
    def post_initiate_payment(self, body):
        return self.post("/payments/", {}, body)

    # NOT TESTED
    def delete_payment(self, account_number: str, payment_id: str):
        return self.delete("/payments/" + account_number + "/pending-payments/" + payment_id, {})


class PaymentDto:
    def __init__(self, kid: [str, None],
                 debit_account_number: str,
                 credit_account_number: str,
                 amount: float,
                 requested_execution_date: str,
                 country: [str, None],
                 currency: [str, None],
                 immediate_payment: [bool, None]):

        self.kid = kid
        self.debitAccountNumber = debit_account_number
        self.creditAccountNumber = credit_account_number
        self.amount = amount,
        self.requestedExecutionDate = requested_execution_date
        self.country = country
        self.currency = currency
        self.immediatePayment = immediate_payment
