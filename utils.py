"""
This is utility library.
All REST API calls will be called from this library
"""

import json
import logging
import time
import requests


logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(logging.WARNING)
requests.packages.urllib3.disable_warnings()

logger = logging.getLogger('utils')
logger.addHandler(logging.NullHandler())


class NoAuth(requests.auth.AuthBase):
    """This "authentication" handler exists for use with custom authentication
    systems, such as the one for the NBFS API.  It simply passes the
    Authorization header as-is.  The default authentication handler for
    requests will clobber the Authorization header."""

    def __call__(self, r):
        return r


def authenticate(provider, username, password):
    """
    Function to get token for authentication
    Params:
        provider:  API_GATEWAY_IP
        username:  APPLIANCE_ADMIN_USERNAME
        password:  APPLIANCE_ADMIN_PASSWORD
    """
    headers = {"Content-Type": "application/json"}
    data = {"userName": username, "password": password}
    data = json.dumps(data)
    session1 = requests.session()
    session1.verify = False
    session1.auth = NoAuth()
    auth_url = "https://{}:14161/api/appliance/v1.0/authentication/" \
               "login".format(provider)
    response = session1.post(auth_url, headers=headers, data=data)
    return session1, response.json()['token']


def get_url(provider, tail):
    """
    This function will construct the base URL for REST API execution
    """
    api_root = 'https://{}:14161'.format(provider)
    return api_root + tail


def run_api(provider, url, username, password,
            req_type='post', data=None):
    """
    This function will execute REST APIs
    """
    (session, token) = authenticate(provider, username, password)

    headers = {"Content-Type": "application/json"}
    headers.update({"Authorization": "Bearer {}".format(token)})

    url = get_url(provider, url)
    if req_type == 'post':
        if isinstance(data, dict):
            data = json.dumps(data)
            print(data)
        response = session.post(url, headers=headers,
                                data=data)
        print(response.json())

        # Waiting for task to be completed
        task_flag = False
        if response.json()["taskId"]:
            task_id = response.json()["taskId"]
            for timeout in range(150):
                print("Waiting for [{}] to complete..".format(task_id))
                url = "/api/appliance/v1.0/tasks/{}".format(task_id)
                task_url = get_url(provider, url)
                task_response = session.get(task_url, headers=headers)
                if task_response.json()["data"]["attributes"][
                    "state"] == "SUCCESS":
                    task_flag = True
                    break
                time.sleep(60)
        if task_flag:
            return True
        else:
            raise "Operation failed"

    if req_type == 'get':
        response = session.get(url, headers=headers)

    if req_type == 'delete':
        response = session.delete(url, headers=headers,
                                  data=None)

    logger.info("REST EndPoint: {}".format(url))
    logger.info("Payload: {}".format(data))
    logger.info("Request Type: {}".format(req_type))
    json_obj = json.loads(response.text)
    logger.info("Request Response: {}".format(json.dumps(json_obj)))

    if response.status_code not in (200, 202):
        raise Exception("Request failed with {}".format(response))
    return response.json()
