import pandas as pd
from db import fetch_msisdn_to_imei

def get_imei_data(msisdn: list, username: str) -> dict:
    """
    Fetch IMEI data for given user.
    Each user only gets results for their own request.
    """
    df = fetch_msisdn_to_imei(msisdn)

    if df.empty:
        return {
            "status":    "success",
            "requested_by": username,
            "count":     0,
            "data":      []
        }

    # Clean NaN values so JSON serialization doesn't fail
    df = df.replace({pd.NA: None, float("nan"): None})

    return {
        "status":       "success",
        "requested_by": username,   # user 
        "count":        len(df),
        "data":         df.to_dict(orient="records")
    }