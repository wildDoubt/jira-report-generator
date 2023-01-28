import requests
import json
import pandas as pd
from datetime import datetime
from typing import Callable


def save_response_to_csv(
    file_name: str, response: requests.Response, _filter: Callable[[dict], dict]
):
    now_time = datetime.now()
    current_date = now_time.strftime("%Y-%m-%d")
    current_datetime = now_time.strftime("%H_%M_%S")

    json_object = json.loads(response.text)
    filtered_objects = list(map(_filter, json_object["issues"]))
    df = pd.DataFrame.from_dict(filtered_objects)
    df.to_csv(
        f"[{current_date}]{file_name}-{current_datetime}.csv",
        index=False,
        encoding="utf-8-sig",
    )
