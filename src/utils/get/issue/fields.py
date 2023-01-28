import requests
import json
from requests.auth import HTTPBasicAuth


def _filter(obj: dict):
    return (obj["name"], obj["key"])


def get_issue_fields(url: str, auth: HTTPBasicAuth, headers):
    response = requests.request("GET", url, headers=headers, auth=auth)
    json_object = json.loads(response.text)

    issue_fields_name_by_key = dict(map(_filter, json_object))

    return issue_fields_name_by_key
