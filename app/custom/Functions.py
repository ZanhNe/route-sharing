from app.extentions.extentions import geocoder, client
from app.GUI.model.models import Location
from typing import List
from openrouteservice.directions import directions
from pprint import pprint

def get_coordinate(query: str):
    results = geocoder.geocode(query=query)
    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    return lat, lng   


def get_direction(first_location: Location, second_location: Location):
    first_coord = [first_location.longitude, first_location.latitude]
    second_coord = [second_location.longitude, second_location.latitude]
    try:
        route = directions(client=client, coordinates=[first_coord, second_coord], format='geojson')
        return route
    except Exception as e:
        print(e)
        return None
    