import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout

import json

from local_credentials import CLIENT_ID, CLIENT_SECRET


def get_api_token():
    access_response = requests.post(
        'https://us.battle.net/oauth/token',
        auth=HTTPBasicAuth(
            CLIENT_ID,
            CLIENT_SECRET
        ),
        params={
            'grant_type': 'client_credentials'
        }
    )

    ACCESS_TOKEN = json.loads(access_response.content).get('access_token')

    return ACCESS_TOKEN


def api_response(url, token):
    try:
        result = requests.get(
            url+token,
            timeout=10
        )
        return result, True

    except Timeout as err:
        return err, False


