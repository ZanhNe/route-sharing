import httpx
from app.extentions.extentions import key_ors

url_openroute_direction = 'https://api.openrouteservice.org/v2/directions/driving-car/geojson'

async def get_direction_ORS(data):
    async with httpx.AsyncClient() as client:
        try:
            headers = {'Authorization': key_ors, 'Content-type': 'application/json'}
            response = await client.post(url=url_openroute_direction, headers=headers, content=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            return {"error": f"HTTP error: {exc.response.text}"}
        except httpx.RequestError as exc:
            return {"error": f"Request error: {exc}"}          

