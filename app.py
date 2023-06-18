from chalice import Chalice, Response
import logging
from create_dynamodb import aws
from utills.utills import (
    valid_string,
    api_call
)
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

app = Chalice(app_name="weather-api")
base_url = os.environ.get("BASE_URL", "http://api.weatherstack.com/current")
api_key = os.environ.get("API_KEY", "<API_KEY>")


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
    if valid_string(location):
        response = api_call(base_url, api_key, location)
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

    if valid_string(location):
        response = api_call(base_url, api_key, location)
        aws_connect: aws = aws()
        dynamodb = aws_connect.dynamodb
        table = dynamodb.Table("Weather_Data")

        
        if response.get("success") is False:
            return Response(
                status_code=502, body=response, headers={"Content-Type": "application/json"}
            )

        db_response = table.put_item(
        Item={
            "location": str(response.get("location").get("name")).lower(),
            "location_info": response.get("location"),
            "request": response.get("request"),
            "current": response.get("current"),
        }
    )
        logger.info(f"db_response{db_response}")
        return Response(
            status_code=201,
            body={"response": "Successfully saved data"},
            headers={"Content-Type": "application/json"},
        )

    return Response(
            status_code=400,
            body={"response": "Please enter valid location name"},
            headers={"Content-Type": "application/json"},
        )


@app.route("/weather_data/{location}")
def get_weather_data(location :str):
    aws_connect: aws = aws()
    dynamodb = aws_connect.dynamodb
    table = dynamodb.Table("Weather_Data")
    if valid_string(location):
        db_response = table.get_item(Key={"location": location.lower()})
        response = db_response.get("Item")
        if response is None:
            return Response(
                status_code=404,
                body={"response": f"data not found for location: {location}"},
                headers={"Content-Type": "application/json"},
            )
        else:
            return Response(
        status_code=200, body=response, headers={"Content-Type": "application/json"}
    )
    return Response(
                status_code=400,
                body={"response": "Please enter valid location name"},
                headers={"Content-Type": "application/json"},
            )

