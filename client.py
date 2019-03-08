from PersonClient import *
import requests

# Paths:
_loc_branch = "/locations/branches/"
_loc_atm = "/locations/atms/"

# Load keys:
load_dotenv()
_client_id = os.environ.get("CLIENT_ID")
_client_secret = os.environ.get("CLIENT_SECRET")
_api_key = os.environ.get("API_KEY")


class BaseClient:
    def __init__(self):
        aws_signing_v4 = AwsSigningV4(
            aws_access_key_id=_client_id,
            aws_secret_access_key=_client_secret,
            aws_host="developer-api-sandbox.dnb.no",
            aws_region="eu-west-1",
            aws_service="execute-api",
        )
        self.url_header_generator = UrlHeaderGenerator(
            endpoint="https://developer-api-sandbox.dnb.no",
            aws_signing_v4=aws_signing_v4,
        )

    def get(self, path, query_parameters=None, api_token=None):
        if query_parameters is None:
            query_parameters = {}

        url, headers = self.url_header_generator.generate(
            path=path, params=query_parameters, method="GET", api_key=_api_key, api_token=api_token
        )
        return requests.get(url, headers=headers)


class GeneralClient(BaseClient):

    # Currency:

    def get_currency_list(self, from_currency: str):
        if len(from_currency) != 3:
            raise AttributeError("currency must be string of length 3")
        from_currency = from_currency.upper()

        return self.get("/currencies/" + from_currency)

    def get_currency_rate(self, from_currency: str, to_currency: str):
        path = "/currencies/{}/convert/{}".format(from_currency, to_currency)
        return self.get(path)

    # Branches:

    def get_branches_list(self):
        return self.get(_loc_branch)

    def get_atm_list(self):
        return self.get(_loc_atm)

    def get_closest_branch(self, latitude: [str, float], longitude: [str, float]):
        return self.__get_closest__(_loc_branch, latitude, longitude)

    def get_closest_atm(self, latitude: [str, float], longitude: [str, float]):
        return self.__get_closest__(_loc_atm, latitude, longitude)

    def __get_closest__(self, path, latitude, longitude):
        latitude = str(latitude)
        longitude = str(longitude)
        return self.get(path + "coordinates", {"latitude": latitude, "longitude": longitude})

    def get_branch_details(self, branch_id: [int, str]):
        return self.get(_loc_branch + str(branch_id))

    def get_closest_branch_address(self, address: str):
        print("NOT IMPLEMENTED")
        return ""

    # Test customers:

    def get_test_customers(self):
        return self.get("/testCustomers/")
