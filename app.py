from chalice import Chalice, Response
import requests
import boto3
import logging
from create_dynamodb import aws
from utills.utills import (
    valid_string,
    api_call,
    chalice_response,
)
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Chalice(app_name="weather-app")
base_url = os.environ.get("BASE_URL", "http://api.weatherstack.com/current")
api_key = os.environ.get("API_KEY", "6d6be3d929a588807e3d5ef2c3a4cc3a")  # TO_REMOVE


@app.route("/")
def index():
    return Response(
        status_code=200,
        body={
            "response": "welcome to weather api, please go through the readme for more info"
        },
        headers={"Content-Type": "application/json"},
    )


@app.route("/weather/{location}")
def weather(location):
    if not valid_string(location):
        logger.info("procceding")
        response = api_call(base_url, api_key, location)
        # logger.info(f"response{response.get('success')}")
        if response.get("success") is False:
            return Response(
                status_code=502,
                body=response,
                headers={"Content-Type": "application/json"},
            )

        return Response(
            status_code=200, body=response, headers={"Content-Type": "application/json"}
        )
    else:
        return Response(
            status_code=400,
            body={"response": "Please enter valid location name"},
            headers={"Content-Type": "application/json"},
        )


@app.route("/weather", methods=["POST"])
def store_weather_location():
    location = app.current_request.json_body.get("location")
    logger.info(location)
    response = api_call(base_url, api_key, location)

    if response.get("success") is False:
        return Response(
            status_code=502, body=response, headers={"Content-Type": "application/json"}
        )

    aws_connect: aws = aws()
    dynamodb = aws_connect.dynamodb
    table = dynamodb.Table("Weather_Data")
    db_response = table.put_item(
        Item={
            "location": response.get("location").get("name"),
            "location_info": response.get("location"),
            "request": response.get("request"),
            "current": response.get("current"),
        }
    )
    print(f"db_response{db_response}")
    return Response(
        status_code=201,
        body={"response": "Successfully saved data"},
        headers={"Content-Type": "application/json"},
    )


@app.route("/weather_data/{location}")
def get_weather_data(location):
    logger.info(app.current_request.json_body)
    aws_connect: aws = aws()
    dynamodb = aws_connect.dynamodb
    table = dynamodb.Table("Weather_Data")
    db_response = table.get_item(Key={"location": location})
    response = db_response.get("Item")
    logger.info(db_response)
    logger.info(response)
    if not valid_string(location):
        return Response(
            status_code=400,
            body={"response": "Please enter valid location name"},
            headers={"Content-Type": "application/json"},
        )
    elif response is None:
        return Response(
            status_code=404,
            body={"response": f"data not found for location: {location}"},
            headers={"Content-Type": "application/json"},
        )

    return Response(
        status_code=200, body=response, headers={"Content-Type": "application/json"}
    )


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
