"""
To use, you will have to set up an AWS account and authenticate with boto3.
"""
import pandas as pd
import boto3
import json

from decimal import Decimal
from time import sleep
from tqdm import tqdm


def main(df, table_name, create_table=False):
    dynamodb = boto3.resource('dynamodb')
    if create_table:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'client_id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'client_id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        sleep(10)
    table_name = dynamodb.Table(table_name)
    df.fillna(value='', inplace=True)
    data = df.T.to_dict()
    data = json.loads(json.dumps(data), parse_float=Decimal)
    for key, value in tqdm(data.items()):
        table_name.put_item(Item=value)


if __name__ == "__main__":
    df = pd.DataFrame({
        "client_id": [13],
        "job": [100000],
        "zip_code": ["64105"]
    })

    main(df, 'people_sample', create_table=True)
