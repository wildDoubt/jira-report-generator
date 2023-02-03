import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
import json
import pandas as pd

from src.utils import get_issue_fields, get_issues, save_df_csv, process_column_cases

load_dotenv(verbose=True)

DOMAIN = os.getenv("DOMAIN")
GET_ISSUES_BY_JQL_URL = f"https://{DOMAIN}.atlassian.net/rest/api/3/search"
GET_ISSUE_FIELD_URL = f"https://{DOMAIN}.atlassian.net/rest/api/3/field"
ISSUE_KEY = "Key"


def create_params(jql, fields, name_key_map, start_at=0, max_results=100):
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


def task(fields, response, prev_result, name_key_map):
    prev_result = pd.concat([prev_result, get_issues(response, fields, name_key_map)])

    total = response["total"]
    start_at = response["startAt"]
    max_results = response["maxResults"]
    return prev_result, total, start_at, max_results


def beautify_result(obj):
    for field_name in fields:
        if field_name == ISSUE_KEY:
            continue

        obj[field_name] = obj[field_name].apply(process_column_cases[field_name])

    return obj


def initialize_variables():
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

    filename, jql, fields = mock_input.values()
    fields = [ISSUE_KEY] + fields
    params = create_params(jql, fields, name_key_map)

    # get issues
    response = get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params)
    return name_key_map, filename, fields, params, response


if __name__ == "__main__":
    # prepare params and fields
    (
        name_key_map,
        filename,
        fields,
        params,
        response,
    ) = initialize_variables()

    # process issues
    result = pd.DataFrame()
    while True:
        result, total, start_at, max_results = task(
            fields, response, result, name_key_map
        )

        result = beautify_result(result)

        if total > start_at + max_results:
            params["startAt"] = start_at + max_results
            response = get_issues_by_jql(GET_ISSUES_BY_JQL_URL, auth, headers, params)
            continue
        break

    # save issues
    save_df_csv(filename, result)
