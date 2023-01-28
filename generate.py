import requests
from requests.auth import HTTPBasicAuth
from src.utils import get_issue_fields, save_response_to_csv
from dotenv import load_dotenv
import os
import json

# load environment variables
load_dotenv(verbose=True)

DOMAIN = os.getenv("DOMAIN")
GET_ISSUES_BY_JQL_URL = f"https://{DOMAIN}.atlassian.net/rest/api/3/search"
GET_ISSUE_FIELD_URL = f"https://{DOMAIN}.atlassian.net/rest/api/3/field"
ISSUE_KEY = "Key"

auth = HTTPBasicAuth(
    os.getenv("USER_EMAIL"),
    os.getenv("USER_API_TOKEN"),
)

headers = {"Accept": "application/json"}

# Column name -> key로 변환하기 위한 딕셔너리
name_key_map = get_issue_fields(GET_ISSUE_FIELD_URL, auth, headers)

mock_input = {
    "filename": os.getenv("FILENAME"),
    "jql": os.getenv("JQL"),
    "fields": json.loads(os.getenv("FIELDS")),
}


def create_params(jql, fields):
    params = {
        "jql": jql,
        "fields": list(map(lambda x: name_key_map[x], fields)),
        "fieldsByKeys": True,
        "maxResults": 100,
    }

    return params


def get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params):
    return requests.request(
        "GET", GET_ISSUES_BY_JQL_URL, headers=headers, params=params, auth=auth
    )


def _filter(obj: dict):
    global fields
    return dict(
        zip(
            fields,
            [
                obj["fields"][name_key_map[field_name]]
                if field_name != ISSUE_KEY
                else obj["key"]
                for field_name in fields
            ],
        )
    )


if __name__ == "__main__":
    filename, jql, fields = mock_input.values()
    fields = [ISSUE_KEY] + fields

    params = create_params(jql, fields)
    response = get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params)
    save_response_to_csv(filename, response, _filter)
