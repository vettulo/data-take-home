import aiohttp
import asyncio

from fastapi import FastAPI


app = FastAPI()
ENDPOINTS = ['http://0.0.0.0:8000/api1/v1/', 'http://0.0.0.0:8000/api2/v1/', 'http://0.0.0.0:8000/api3/v1/']

DEDUCTIBLE = 'deductible'
STOP_LOSS = 'stop_loss'
OOP_MAX = 'oop_max'


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data


async def process_api_endpoints(member_id: int):
    fetch_coroutines = []
    for endpoint in ENDPOINTS:
        url = f'{endpoint}&member_id={member_id}'
        fetch_coroutines.append(asyncio.Task(fetch_url(url)))

    responses = await asyncio.gather(*fetch_coroutines)

    deductibles = 0
    stop_losses = 0
    oop_maxs = 0

    for response in responses:
        deductibles += response.get(DEDUCTIBLE, 0)
        stop_losses += response.get(STOP_LOSS, 0)
        oop_maxs += response.get(OOP_MAX, 0)

    qty = len(responses)
    response = {
        DEDUCTIBLE: int(deductibles / qty),
        STOP_LOSS: int(stop_losses / qty),
        OOP_MAX: int(oop_maxs / qty),
    }
    return response


@app.get("/")
async def root(member_id: int):
    response = await process_api_endpoints(member_id)
    return response
