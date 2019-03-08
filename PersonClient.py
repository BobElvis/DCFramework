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

    def get_accounts(self):
        return self.get("/accounts/", {})
