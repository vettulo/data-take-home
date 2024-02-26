import logging
from datetime import date

import httpx
from fastapi import FastAPI, status
from pydantic import BaseModel

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
async def root(request_params: CoverageRequest):
    clearinghouse_response = await get_clearinghouse_response(request_params)

    return clearinghouse_response
