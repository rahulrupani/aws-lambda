import boto3
from datetime import datetime, timedelta
import time
import json
from json2html import *
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('logs')

# Query which will be executed via lambda 
# you can rewrite the query as per your requirement.
query = "fields @timestamp, @message | filter action == 'BLOCK' | sort @timestamp desc"

# Name of the Log Group which need to be monitored 
log_group = '/aws/ecs-service/service-LogGroupName' #***

# Executing query and collecting the response 
# you can configure start and end time of the query as per your need, we have configue to 
# check last 1hr logs which actions are Blocked #***
start_query_response = client.start_query(
    logGroupName=log_group,
    startTime=int((datetime.today() - timedelta(hours=1)).timestamp()),
    endTime=int(datetime.now().timestamp()), 
    queryString=query,
)
# Capturing query Id to check the status, also printing query id.
query_id = start_query_response['queryId']
print('This is the request id :- ' + query_id)

#Declaring variable to be used later
response = None
Status = "status"

# Cheking the status if the query is completed
while response == None or response['status'] == 'Running':
    print('Waiting for query to complete ...')
    time.sleep(1)
    response = client.get_query_results(
        queryId=query_id
    )

"""
Update the feilds as per your need 
To:- email id
HeadBlock :- If the condition is satisfied and there are block request or if condition satisfy.
HeadNoBlock :- If the condition is not satisfied and there are no blocked request.
"""

TO = [ 'YourEmailId@YourDomain.com','YourEmailI2d@YourDomain.com'] #***
HeadBlock = "<h1 style='text-align:Left'> Hello!<br> There are <span style='color: #FF0000'>Blocked requests</span> in the logs since last 1hr </p> </h1>" #***
HeadNoBlock = "<h1 style='text-align:Left'> Hello!<br> There are <span style='color: #008000'>No Blocked requests</span> in the logs since last 1hr </p> </h1>" #***

# No need to change below values, only change if you know what need to be updated.
data = json.dumps(response['results']) # Extracting the data from qurey response.
htmlbody = json2html.convert(json = data) # Converting results into html.

# Email Footer 
htmlbody = (htmlbody + '<br><br><h3> Regards<br>Lambda Notification </h3>') #***


if not response['results']:
    print('There are no Blocked requests in last 1hrSending email')
    heading = HeadNoBlock
    subject = "Notification || No Blocked Request"
    print(heading)
    print(subject)
else:
    print('There are Blocked requests in last 1hr, Sending email')
    heading = HeadBlock
    subject = "Notification || Blocked Request"
    print(heading)

def send_html_email():
    #update region_name
    ses_client = boto3.client("ses", region_name="region")
    CHARSET = "UTF-8"
    HTML_EMAIL_CONTENT = ( 
        "<html>" + "<head></head>" + heading + "<p>" + htmlbody + "</p> </body> </html> "
        )

    response = ses_client.send_email(
        Destination={
            "ToAddresses": TO
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": HTML_EMAIL_CONTENT,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": subject,
            },
        },
        # Source should be the sender of the request
        Source="Lambda Notification <lambda@YourDomain.com>", #***
    )
Status = "status"
def lambda_handler(event, lambda_context):
    if not response['results']:
        print('There are no Blocked requests in last 1 hr, No email will be sent')
        print(data)
        print(htmlbody)
        print("There is No data")
        heading = HeadNoBlock
        print(heading)
        send_html_email()
    else:
        print('There are Blocked requests in last 1 hr, Sending email')
        print(htmlbody)
        print("There is data")
        heading = HeadBlock
        print(heading)
        send_html_email()
    return { 
        Status : response
    }