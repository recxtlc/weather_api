import requests
from requests.exceptions import ConnectTimeout


def valid_string(location: str) -> bool:
    try:
        float(location)
        return False
    except ValueError:
        return True


def api_call(base_url: str, api_key: str, location: str) -> dict:
    try: 
        params = {
        'access_key': api_key,
        'query': location
        }
        response = requests.get(url=base_url,timeout=15,params=params)
        return response.json()
    except ConnectTimeout as err:
        print('Request has timed out')

