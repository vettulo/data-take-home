import logging

import httpx
from analytics import write_to_analytics
from fastapi import FastAPI, Header, status
from models import CoverageRawModel, CoverageRequest
from mongo import write_to_mongo
from overrides import get_overrides
from pydantic import BaseModel

CLEARINGHOUSE_URL = "http://clearinghouse_api:8001"

app = FastAPI()

logger = logging.getLogger()


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
async def root(
    request_params: CoverageRequest,
    customer_id: str = Header(None, convert_underscores=True),
):
    clearinghouse_response = await get_clearinghouse_response(request_params)

    overrides = get_overrides(request_params.member_id, request_params.member_dob)

    merged_result = {
        "copay": overrides.get("copay") or clearinghouse_response.get("copay"),
        "coinsurance": overrides.get("coinsurance")
        or clearinghouse_response.get("coinsurance"),
        "deductible": overrides.get("deductible")
        or clearinghouse_response.get("deductible"),
        "oop_max": overrides.get("oop_max") or clearinghouse_response.get("oop_max"),
    }

    await write_to_mongo(
        {
            "customer_id": customer_id,
            "request": request_params.dict(),
            "response": merged_result,
        }
    )

    clearinghouse_result = {
        "copay": clearinghouse_response.get("copay"),
        "coinsurance": clearinghouse_response.get("coinsurance"),
        "deductible": clearinghouse_response.get("deductible"),
        "oop_max": clearinghouse_response.get("oop_max"),
    }

    logger.info("Writing to mongo: %s", overrides)

    logger.info(bool(overrides))
    write_to_analytics(
        CoverageRawModel(
            customer_id=customer_id,
            member_id=request_params.member_id,
            member_dob=request_params.member_dob,
            payer_id=request_params.payer_id,
            response_copay=merged_result.get("copay"),
            response_coinsurance=merged_result.get("coinsurance"),
            response_deductible=merged_result.get("deductible"),
            response_oop_max=merged_result.get("oop_max"),
            ch_response_copay=clearinghouse_result.get("copay"),
            ch_response_coinsurance=clearinghouse_result.get("coinsurance"),
            ch_response_deductible=clearinghouse_result.get("deductible"),
            ch_response_oop_max=clearinghouse_result.get("oop_max"),
            overriden=bool(overrides),
        )
    )

    return merged_result
