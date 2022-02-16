import os
import time
import jwt
import requests


def get_token():
    service_account_id = os.environ.get('YC_SERVICE_ACCOUNT_ID')
    key_id = os.environ.get('YC_SERVICE_KEY_ID')

    private_key = os.environ.get('YC_JWT_PRIVATE_KEY')

    now = int(time.time())
    payload = {
        'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
        'iss': service_account_id,
        'iat': now,
        'exp': now + 360}

    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': key_id})

    IAM_token = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', json={"jwt": encoded_token})
    return IAM_token.json()


print(get_token())
