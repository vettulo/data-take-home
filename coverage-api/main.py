import logging

import httpx
from fastapi import FastAPI, Header, status
from pydantic import BaseModel

from overrides import get_overrides
from mongo import write_to_mongo

CLEARINGHOUSE_URL = "http://clearinghouse_api:8001"

app = FastAPI()

logger = logging.getLogger()


class CoverageRequest(BaseModel):
    member_id: str
    member_dob: str
    payer_id: str


async def get_clearinghouse_response(request_params: CoverageRequest):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                CLEARINGHOUSE_URL,
                # headers=self.headers,
                # timeout=self.REQUEST_TIMEOUT_IN_SECONDS,
                json=request_params.dict(),
            )
            return response.json()
        except httpx.TimeoutException:
            logger.exception("{SERVICE_NAME} request timeout")
            return {
                "status": status.HTTP_502_BAD_GATEWAY,
                "message": {"error": "Timeout"},
            }


@app.post("/")
async def root(request_params: CoverageRequest, customer_id: str = Header(None, convert_underscores=True)):
    clearinghouse_response = await get_clearinghouse_response(request_params)

    overrides = get_overrides(request_params.member_id, request_params.member_dob)

    merged_result = {
        "copay": overrides.get("copay") or clearinghouse_response.get("copay"),
        "coinsurance": overrides.get("coinsurance") or clearinghouse_response.get("coinsurance"),
        "deductible": overrides.get("deductible") or clearinghouse_response.get("deductible"),
        "oop_max": overrides.get("oop_max") or clearinghouse_response.get("oop_max"),
    }

    await write_to_mongo({
        "customer_id": customer_id,
        "request": request_params.dict(),
        "response": merged_result
    })
    return merged_result
