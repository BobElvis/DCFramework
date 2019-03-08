import json
from PersonClient import Person


def main():
    p = Person(29105573083)
    print(json.dumps(p.get_accounts().json(), indent=4, sort_keys=False))


if __name__ == "__main__":
    main()
