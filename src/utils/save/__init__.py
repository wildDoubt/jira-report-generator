from datetime import datetime
import pandas as pd


def save_df_csv(filename: str, result: pd.DataFrame):
    now_time = datetime.now()
    current_date = now_time.strftime("%Y-%m-%d")
    current_datetime = now_time.strftime("%H_%M_%S")

    result.to_csv(
        f"[{current_date}]{filename}-{current_datetime}.csv",
        index=False,
        encoding="utf-8-sig",
    )
