from collections import defaultdict

change_first_response_column_format = (
    lambda x: x.get("ongoingCycle").get("remainingTime").get("friendly", "None")
)
change_organization_column_format = lambda x: x[0].get("name", "None")
change_email_column_format = lambda x: x.get("emailAddress", "None")
change_date_column_format = lambda x: x.split(".")[0].replace("T", " ")


def return_argument(arg):
    return arg


# default value is a function that returns parameter itself
process_column_cases = defaultdict(
    lambda: return_argument,
    {
        "Time to first response": change_first_response_column_format,
        "Organizations": change_organization_column_format,
        "Reporter": change_email_column_format,
        "Created": change_date_column_format,
        "Updated": change_date_column_format,
    },
)
