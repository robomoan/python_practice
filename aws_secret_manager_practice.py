'''
Code reference
AWS Secret Manager Console Sample Code:
https://ap-northeast-2.console.aws.amazon.com/secretsmanager/
'''

import os
import boto3
from botocore.exceptions import ClientError

def get_secret():

    secret_name = 'example'
    region_name = 'ap-northeast-2'

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Save SecretString as .env file
    path = os.path.join(os.getcwd(), '.env')
    with open(path, 'w') as file:
        file.write(secret)

if __name__ == '__main__':
    get_secret()
