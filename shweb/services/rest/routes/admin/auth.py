import hmac
import hashlib
import base64


from flask import current_app
import boto3


def get_secret_hash(username, client_id, client_secret,):
    msg = username + client_id
    dig = hmac.new(str(client_secret).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def change_password_challenge(
    user_pool_id,
    client_id,
    client_secret,
    aws_access_key_id,
    aws_secret_access_key,
    username,
    temp_password,
    new_password,
):
    secret_hash = get_secret_hash(username, client_id, client_secret)
    cognito = boto3.client(
        'cognito-idp',
        region_name=current_app.config['AWS_REGION'],
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    auth_response = cognito.admin_initiate_auth(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        AuthFlow='ADMIN_NO_SRP_AUTH',
        AuthParameters={
            'USERNAME': username,
            'SECRET_HASH': secret_hash,
            'PASSWORD': temp_password
        }
    )

    if 'ChallengeName' not in auth_response:
        raise Exception('This user has already changed the password')

    if auth_response['ChallengeName'] != 'NEW_PASSWORD_REQUIRED':
        raise Exception("This script supports only the 'NEW_PASSWORD_REQUIRED' challenge")

    challenge_response = cognito.admin_respond_to_auth_challenge(
        UserPoolId=user_pool_id,
        ClientId=client_id,
        ChallengeName=auth_response['ChallengeName'],
        Session=auth_response['Session'],
        ChallengeResponses={
            'USERNAME': username,
            'NEW_PASSWORD': new_password,
            'SECRET_HASH': secret_hash,
            'userAttributes.nickname': username
        }
    )

    return username, new_password, challenge_response
