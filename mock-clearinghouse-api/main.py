import datetime
import logging

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

logger = logging.getLogger()


class ClearinghouseRequest(BaseModel):
    member_id: str
    member_dob: str
    payer_id: str


@app.post("/")
async def root(request_params: ClearinghouseRequest):
    logger.info("Clearinghouse request", extra=request_params.dict())
    print("clearinghouse request", request_params.dict())
    # TODO: parameterize this so it's not hard-coded
    return {
        "copay": 1500,
        "coinsurance": None,
        "deductible": None,
        "oop_max": 500000,
        **request_params.dict()
    }

