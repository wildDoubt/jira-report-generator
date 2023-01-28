import pandas as pd
from typing import Callable


def get_issues(response, _filter: Callable[[dict], dict]):
    filtered_objects = list(map(_filter, response["issues"]))
    return pd.DataFrame.from_dict(filtered_objects)
