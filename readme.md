# Weather API with DynamoDB Integration

This API connects to weather API, retrieves weather data, and stores it into DynamoDB.

## Table of Contents

- [projec Description](#project-description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Design decisions ](#design-decisions )
- [Assumptions made during the development](#assumptions-made-during-the-development)

## Project Description

This project provides a RESTful API that integrates with a weather API to restrive weather data for a given location. The restrived data us then stored in DynamoDB for further usage. The API provides endpoints to retrieve weather information.

## Features

- Retrieve weather information from a weather api, for a specific location.
- Store weather data into DynamoDB.
- Retrieve weather information from a DynamoDB.

## Prerequisites

Before running this project, ensure you have the following prerequisites:

- Docker
- Python 3.9.13 or greater
- API key for the weather API [WEATHERSTACK](https://weatherstack.com)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/recxtlc/weather_api.git
   cd weather api
   ```

2. Start and run docker container for DynamoDB local instance
   ```bash
   docker-compose up
   ```
3. Create and activate a virtual environment:

   ```bash
   # open new terminal
   python3 -m venv venv
   source venv/bin/activate # for linux
   venv\Script\activate  # for Windows
   ```

4. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the API, you need to configure the following settings:

1. Weather API key: Obtain an API key from the weather API provider [WEATHERSTACK](https://weatherstack.com/documentation) and update api key variable in `app.py` <b>line 18<b/>

## Usage

1. Run the API using chalice cmd:

   ```bash
   chalice local --port=8001
   ```

2. The API will be available at `http://localhost:8001` by default. You can test the API using tools like cURL or Postman and Thunderclient (vs code extension).

## API Endpoints

- `GET /weather/{location}`: Retrieves the weather information for the specified location from weather API.
- `POST /weather/{location}`: Add location data from weather API into DynamoDB.
- `GET /weather_data/{location}`: Retrieves the weather information for the specified location from DynamoDB.

# Design decisions 
- Decided to use docker instead of using moto, nice documentation about how to use the docker container can be found here [aws_local_dynamodb_setup](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)
- chalice will not work on default port, cause the port is used by docker container.
# Assumptions made during the development
- How to handle any error that occurs in the weather API, one issue found in their documentation, their error code is using internal error types such as 101 means `missing_access_key` while HTTP method status code 101 means `Switching Protocols`, this was a challenge and I ended up using 502 as status code to handle all errors that occur from the weather.
