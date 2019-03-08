from client import GeneralClient
from PersonClient import Person
import json


def print_dict(response_json: dict):
    print(json.dumps(response_json, indent=2))


def demo():
    client = GeneralClient()

    # Currency:

    #print_dict(client.get_currency_list("NOK").json())
    #print_dict(client.get_currency_rate("NOK", "USD").json())

    # Location:

    latitude = 63.417509
    longitude = 10.405062

    #print_dict(client.get_branches_list().json())
    #print_dict(client.get_atm_list().json())
    #print_dict(client.get_closest_branch(longitude, latitude).json())
    #print_dict(client.get_closest_atm(longitude, latitude).json())
    #print_dict(client.get_branch_details(client.get_closest_branch(latitude, longitude).json()[0]["id"]).json())
    #print_dict(client.get_closest_branch_address(""))

    # Test customers in the sandbox:
    demo_customers(client)


def demo_customers(client: GeneralClient):
    all_customers = client.get_test_customers().json()["customers"]

    # Show some info for two customers:
    for customer in all_customers[0:2]:
        ssn = customer["ssn"]
        name = customer["customerName"]

        customer_client = Person(ssn)
        accounts = customer_client.get_accounts().json()["accounts"]

        print("Name: {}".format(name))
        for i, account in enumerate(accounts):
            print(" - Account {}: {}".format(i, account["accountNumber"]))


if __name__ == "__main__":
    demo()
