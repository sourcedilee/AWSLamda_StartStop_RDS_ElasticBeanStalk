import boto3
import json
import smtplib
envid=['elastic beanstalk environment identifier']
client = boto3.client('elasticbeanstalk')
def lambda_handler(event, context):
    try:
        for appid in range(len(envid)):
            response = client.terminate_environment(EnvironmentId=str(envid[appid].strip()))
            if response:
                print('Terminating environmen t %s' %str(envid[appid]))
                send_email('[Termainating EB...... Success...]')
            else:
                send_email('[Termainating EB...... Failed...]')
                print('Failed to Terminate environment %s' %str(envid[appid]))
            break
    except Exception as e:
        print(e)



def send_email(subject):
    SENDER = 'sender_email'
    RECIPIENT = 'recipient_email'
    AWS_REGION = 'aws_ses_region'
    SUBJECT = subject
    BODY_TEXT = ("")
    BODY_HTML = """<html>
<head></head>
<body>
  <h1>URL</h1>
  <p>
    <a href='back end URL'>BackEnd</a>
  </p>
</body>
</html>
"""
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])