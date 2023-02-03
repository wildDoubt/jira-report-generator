import pandas as pd
import functools

ISSUE_KEY = "Key"


def process_field_values(issue_object: dict, field_names: list, name_key_map: dict):
    return dict(
        zip(
            field_names,
            get_field_values(issue_object, field_names, name_key_map),
        )
    )

def get_field_values(issue_object, fields, name_key_map):
    return [
                issue_object["fields"][name_key_map[field_name]]
                if field_name != ISSUE_KEY
                else issue_object["key"]
                for field_name in fields
            ]


def get_issues(response, fields, name_key_map) -> pd.DataFrame:
    filtered_objects = list(
        map(
            functools.partial(
                process_field_values, field_names=fields, name_key_map=name_key_map
            ),
            response["issues"],
        )
    )
    return pd.DataFrame.from_dict(filtered_objects)
