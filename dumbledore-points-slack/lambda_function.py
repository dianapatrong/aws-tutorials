import json
import urllib
import time
import os
import hmac
import hashlib
import boto3

dynamo = boto3.resource('dynamodb')

ADMIN = ['dianapatrong']
HOUSES = ["gryffindor", "slytherin", "ravenclaw", "hufflepuff"]
PREFIXES = ["In the lead is ", "Second place is ", "Third place is ", "Fourth place is "]


def verify_request(event):
    body = event['body']
    timestamp = event['headers']['X-Slack-Request-Timestamp']
    slack_signature = event['headers']['X-Slack-Signature']

    sig_basestring = f"v0:{timestamp}:{body}".encode('utf-8')
    my_signature = f"v0={hmac.new(os.environ['SLACK_KEY'].encode('utf-8'), sig_basestring, hashlib.sha256).hexdigest()}"
    return hmac.compare_digest(my_signature, slack_signature)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def lambda_handler(event, context):
    headers = event['headers']
    body = event['body']

    if not verify_request(event):
        return respond(None, {"text": "Message verification failed"})

    table = dynamo.Table('HouseMembers')

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda, ')
    }

