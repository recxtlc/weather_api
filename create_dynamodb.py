import boto3
import botocore.exceptions as boto_exceptions 
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class aws:
    def __init__(self) -> None:
        self.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url="http://localhost:8000",
            region_name="us-west-2",
        )

    def create_dynamodb_table(self):
        try:
            self.dynamodb.create_table(
                TableName="Weather_Data",
                KeySchema=[
                    {"AttributeName": "location", "KeyType": "HASH"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "location", "AttributeType": "S"},
                ],
                ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
            )
        except boto_exceptions.ClientError as err:
            if err.response.get('Error').get('Code') == 'ResourceInUseException':
                logger.info("Table already exists")
            else:
                raise err
            
