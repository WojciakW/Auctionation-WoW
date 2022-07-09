"""
Blizzard API connection resources.
"""

import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import Timeout

import json

from local_credentials import CLIENT_ID, CLIENT_SECRET


def get_api_token():
    """
    Returns Blizzard OAuth token.

    Requires Blizzard API client pre-setup and already generated client ID, Secret.
    """
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


def api_response(url: str, token: str):
    """
    Makes an attempt to connect Blizzard API, fails in case connection hangs for too long.
    Returns a tuple of:
        - API response specified by 'url' param and authorized by Blizz OAuth Token 'token' param,
        - Boolean-type info about connection result.
    """
    try:
        result = requests.get(
            url+token,
            timeout=10
        )
        return result, True

    except Timeout as err:
        return err, False


