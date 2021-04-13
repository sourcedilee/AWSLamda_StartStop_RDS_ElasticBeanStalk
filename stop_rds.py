import sys
import botocore
import boto3
from botocore.exceptions import ClientError
import json
import logging
import smtplib
from datetime import datetime

rds = boto3.client('rds')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    stop_rds_instances('db_instance_identifier')
    return {'statusCode': 200,
            'body': json.dumps('Script execution completed. See Cloudwatch logs for complete output'
                               )}


def stop_rds_instances(dbInstance):
    try:
        now = datetime.now()
        snapName = now.strftime("snap-%m-%d-%Y-%H-%M-%S")
        rds.stop_db_instance(DBInstanceIdentifier=dbInstance, DBSnapshotIdentifier=snapName)
        print ('Success :: stop_db_instance ' + dbInstance)
        send_email('[RDS Termainating...... Success...]')
    except ClientError as e:
        print ('Error :: ' + e.response['Error']['Message'])
        send_email('[RDS Termainating...... Failed...]')
    else:
        print ('RDS Termainated...')


def send_email(subject):
    SENDER = 'sender_email'
    RECIPIENT = 'recipient_email'
    AWS_REGION = 'aws_ses_region'
    SUBJECT = subject
    BODY_TEXT = ''
    BODY_HTML = \
        """<html>
<head></head>
<body>
  <h1>URL</h1>
  <p>
    DB Stopped......
  </p>
</body>
</html>
"""
    CHARSET = 'UTF-8'
    client = boto3.client('ses', region_name=AWS_REGION)
    try:

        # Provide the contents of the email.

        response = \
            client.send_email(Destination={'ToAddresses': [RECIPIENT]},
                              Message={'Body': {'Html': {'Charset': CHARSET,
                                                         'Data': BODY_HTML},
                                                'Text': {'Charset': CHARSET,
                                                         'Data': BODY_TEXT}},
                                       'Subject': {'Charset': CHARSET,
                                                   'Data': SUBJECT}}, Source=SENDER)
    except ClientError as e:
        print (e.response['Error']['Message'])
    else:
        print ('Email sent! Message ID:' + response['MessageId'])
