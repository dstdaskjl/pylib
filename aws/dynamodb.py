import boto3
from typing import Union


class DynamoDB:
    def __init__(self, key_id: str, secret_key: str, region='us-east-1'):
        self.resource = boto3.resource(
            'dynamodb',
            aws_access_key_id=key_id,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def delete(self, table_name: str, pk: str, pk_value: Union[str, int, bytes]) -> dict:
        return self.resource.Table(table_name).delete_item(Key={pk: pk_value})

    def get(self, table_name: str, pk: str, pk_value: Union[str, int, bytes]) -> dict:
        return self.resource.Table(table_name).get_item(Key={pk: pk_value})['Item']

    #  Retrieve the whole table.
    def get_all(self, table_name: str) -> list:
        return self.resource.Table(table_name).scan()['Items']

    def put(self, table_name: str, pk: str, pk_value: Union[str, int, bytes], content: dict) -> dict:
        return self.resource.Table(table_name).put_item(Item={pk: pk_value, **content})
