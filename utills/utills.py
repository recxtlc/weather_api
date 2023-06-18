from chalice import Response
import requests
from requests.exceptions import ConnectTimeout


def valid_string(location: str) -> bool:
    try:
        float(location)
        return True
    except ValueError:
        return False


def api_call(base_url: str, api_key: str, location: str) -> dict:


    try: 

        params = {
        'access_key': api_key,
        'query': location
        }

        api_url = f"{base_url}{api_key}&query={location}"
        response = requests.get(url=base_url,timeout=15,params=params)
        return response.json()
    except ConnectTimeout as err:
        print('Request has timed out')


def chalice_response(body: dict, headers=None, status_code=200) -> Response:
    return Response(
        status_code=status_code,
        body=body,
        headers={"Content-Type": "application/json"}
        if headers is not None
        else headers,  # if headers has a value then use its value
    )
