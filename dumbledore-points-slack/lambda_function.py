import boto3
import os

dynamo = boto3.resource('dynamodb')

SLACK_KEY = bytes(os.environ["SLACK_KEY"], 'utf-8')
