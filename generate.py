import requests
from requests.auth import HTTPBasicAuth
from src.utils import get_issue_fields, get_issues, save_df_csv
from dotenv import load_dotenv
import os
import json
import pandas as pd

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


def create_params(jql, fields, start_at=0, max_results=10):
    params = {
        "jql": jql,
        "fields": list(map(lambda x: name_key_map[x], fields)),
        "fieldsByKeys": True,
        "startAt": start_at,
        "maxResults": max_results,
    }

    return params


def get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params) -> dict:
    return json.loads(
        requests.request(
            "GET", GET_ISSUES_BY_JQL_URL, headers=headers, params=params, auth=auth
        ).text
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


def task(_filter, response, result):
    result = pd.concat([result, get_issues(response, _filter)])

    total = response["total"]
    start_at = response["startAt"]
    max_results = response["maxResults"]
    return result, total, start_at, max_results


if __name__ == "__main__":
    filename, jql, fields = mock_input.values()
    fields = [ISSUE_KEY] + fields

    params = create_params(jql, fields)
    response = get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params)

    result = pd.DataFrame()
    while True:
        result, total, start_at, max_results = task(_filter, response, result)

        if total > start_at + max_results:
            print(f"{start_at} 시작")
            params["startAt"] = start_at + max_results
            response = get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params)
            continue
        break
    save_df_csv(filename, result)
