import datetime
import logging
import random

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
    # TODO: parameterize this so it's not hard-coded

    possible_copays = [1000, 1500, 2000, 2500, 3000, 4000, None]
    possible_coinsurances = [10, 15, 20, 25, 30, 40]
    possible_deductibles = [100000, 200000, 300000, 500000]
    possible_oop_maxes = [300000, 500000, 800000]

    seed_value = hash(request_params.payer_id)
    random.seed(seed_value)
    copay = random.choice(possible_copays)
    return {
        "copay": copay,
        "coinsurance": random.choice(possible_coinsurances) if not copay else None,
        "deductible": random.choice(possible_deductibles) if not copay else None,
        "oop_max": random.choice(possible_oop_maxes) if copay else None,
        **request_params.dict()
    }

