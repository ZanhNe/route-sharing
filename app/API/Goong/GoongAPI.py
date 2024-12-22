import httpx
from app.extentions.extentions import key_goong
from typing import List, Coroutine
import asyncio
import pprint
# from app.utils.utils import logger
import time

BASE_URL = 'https://rsapi.goong.io'
url_detail = f'{BASE_URL}/place/detail'
url_suggest = f'{BASE_URL}/place/autocomplete'

async def get_place_detail_goong(place_id: str):
    async with httpx.AsyncClient() as client:
        try:
            params = {
                'place_id': place_id,
                'api_key': key_goong
            }
            response = await client.get(url=url_detail, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP error: {exc.response.text}"}
        except httpx.RequestError as exc:
            return {"error": f"Request error: {exc}"}

async def get_place_detail(place_id: str):
    async with httpx.AsyncClient() as client:
        try:
            params = {
                'place_id': place_id,
                'api_key': key_goong
            }
            response = await client.get(url=url_detail, params=params)
            response.raise_for_status()
            data = response.json()['result']
            return {
                "place_id": data['place_id'],
                "location": data['geometry']['location'],
                "formatted_address": data['formatted_address']
            }
        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP error: {exc.response.text}"}
        except httpx.RequestError as exc:
            return {"error": f"Request error: {exc}"}

        
async def get_mutiples_place_detail(list_corountine: List[Coroutine]):
    async with httpx.AsyncClient() as client:
            try:
                results = await asyncio.gather(*list_corountine)
                pprint.pprint(object=results)
                return results
            except:
                return None

        
async def get_place_suggest_goong(query: str):
    async with httpx.AsyncClient() as client:
        try:
            params = {
                'input': query,
                'location': '10.8253757, 106.6302426',
                'radius': 30,
                'api_key': key_goong
            }
            response = await client.get(url=url_suggest, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP error: {exc.response.text}"}
        except httpx.RequestError as exc:
            return {"error": f"Request error: {exc}"}


    
        
