import requests
import boto3
from botocore.exceptions import ClientError

url_set = ['https://www.google.com', 'https://www.netflix.com', 'http://uber.net', 'http://upmenu.org', 'https://www.youtube.com']
REGION= "us-east-1"
url_broke= []
SENDER_EMAIL="unixclassd1@gmail.com"
RECEIVER_EMAIL="estephe.kana@utrains.org"

for url in url_set:
    try:
        response = requests.get(url)
        code = response.status_code
        if code == 200:
            print(f"{url} is up and running")
        else: 
            print(f"{url} is down!!")
    except:
        print(f"The url of {url} is unreachable")
        url_broke.append(url)

def send_mail():
    # set a verified email address of dev team
    RECIPIENT = [RECEIVER_EMAIL] # ["<SET A VERIFIED EMAIL OF DEV TEAM>"]
    # set your verified sender email address
    SENDER = SENDER_EMAIL # "<SET A VERIFIED SENDER EMAIL>"
    SUBJECT = "List of endpoints down"
    BODY_TEXT = (f"""
    Hello all,
    Please check the below endpoints as they seem broken
    
    {url_broke}
    Thanks and best regards !!!


    DevOps Team 
    Email: {SENDER_EMAIL}
    """)           
    CHARSET = "UTF-8"
    ses_client = boto3.client('ses', region_name=REGION)
    try:
        response = ses_client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
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
        print(f"Email sent! Message ID: {response['MessageId']}")

# send an email to the dev team if any url is found down

if url_broke:
    send_mail()
else:
    print("All the endpoints are up and running !!!")  
