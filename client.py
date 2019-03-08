from PersonClient import *
import requests

loc_branch = "/locations/branches/"
loc_atm = "/locations/atms/"


class GeneralClient:
    def __init__(self):
        aws_signing_v4 = AwsSigningV4(
            aws_access_key_id=client_id,
            aws_secret_access_key=client_secret,
            aws_host="developer-api-sandbox.dnb.no",
            aws_region="eu-west-1",
            aws_service="execute-api",
        )
        self.url_header_generator = UrlHeaderGenerator(
            endpoint="https://developer-api-sandbox.dnb.no",
            aws_signing_v4=aws_signing_v4,
        )

    def get(self, path, query_parameters=None):
        if query_parameters is None:
            query_parameters = {}

        url, headers = self.url_header_generator.generate(
            path=path, params=query_parameters, method="GET", api_key=api_key, api_token=None
        )
        return requests.get(url, headers=headers)

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
        return self.get(loc_branch)

    def get_atm_list(self):
        return self.get(loc_atm)

    def get_closest_branch(self, latitude: [str, float], longitude: [str, float]):
        return self.__get_closest__(loc_branch, latitude, longitude)

    def get_closest_atm(self, latitude: [str, float], longitude: [str, float]):
        return self.__get_closest__(loc_atm, latitude, longitude)

    def __get_closest__(self, path, latitude, longitude):
        latitude = str(latitude)
        longitude = str(longitude)
        return self.get(path + "coordinates", {"latitude": latitude, "longitude": longitude})

    def get_branch_details(self, branch_id: [int, str]):
        return self.get(loc_branch + str(branch_id))

    def get_closest_branch_address(self, address):
        print("NOT IMPLEMENTED")
        return ""

    # Test customers:

    def get_test_customers(self):
        return self.get("/testCustomers/")
