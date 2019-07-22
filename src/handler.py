import boto3
import datetime
import json
import slack_api.api as SlackApi
from slack_api.admin import users


def lambda_handler(event, context):
    snsclient = boto3.client('sns')
    smclient = boto3.client('secretsmanager')

    slack_token = json.loads(smclient.get_secret_value(SecretId='slack_api')['SecretString'])['oauth_key']

    slackClient = SlackApi.Slack(api_token=slack_token)
    slackua = users.UserAdmin(slackClient)

    datestring = datetime.datetime.now().strftime("%Y%m%d %H:%M:%S")

    slackusers = slackua.list()

    message = f"{datestring} Slack users listed"  # noqa: E501
    snsclient.publish(
        TopicArn="arn:aws:sns:us-east-1:005956675899:test_topic",
        Message=message
    )

    return(slackusers['Resources'])
