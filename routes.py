from fastapi import APIRouter, Depends, HTTPException
from schemas import MSISDNRequest
from services import get_imei_data
from auth import get_current_user
from db import get_latest_date

router = APIRouter()

@router.post("/msisdn-to-imei")
def msisdn_to_imei(
    request: MSISDNRequest,
    username: str = Depends(get_current_user)   # ← Basic Auth here
):
    """
    MSISDN ➡ IMEI 

    Authentication ⏩ HTTP Basic Auth <br>
        Username: "give your username here" <br>
        Password: "password here" <br>

    Request body: <br>
        { <br>
            "msisdn": ["8801XXXXXXXXX"]    
        }
    """
    try:
        result = get_imei_data(
            request.msisdn,
            username
        )
        latest_date = get_latest_date()
        return {
            "requested_by": username,
            "latest_date": latest_date if latest_date else None,
            **result   # keeps your existing data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))