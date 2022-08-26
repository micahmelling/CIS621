import requests
import json


def get_census_data():
    endpoint = "https://api.census.gov/data/2019/pep/charagegroups?get=NAME,POP&HISP=2&for=state:*"
    response = requests.get(endpoint)
    json_output = json.loads(response.text)
    print(json_output)


if __name__ == "__main__":
    get_census_data()
