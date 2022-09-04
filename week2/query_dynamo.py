"""
To use, you will have to set up an AWS account and authenticate with boto3.
"""
import boto3

from boto3.dynamodb.conditions import Attr


def main():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('people_sample')

    response = table.scan(
        FilterExpression=Attr('zip_code').eq('64105')
    )
    items = response['Items']
    print(items)


if __name__ == "__main__":
    main()
