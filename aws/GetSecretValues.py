import boto3
from botocore.exceptions import ClientError


client = boto3.client('secretsmanager')

#Replace the Secret with actual value of secret
secret = client.get_secret_value(
    SecretId='Secret'
)
smtpsecrets = secret['SecretString']
print(smtpsecrets)