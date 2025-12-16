import os, json

import requests
from dotenv import load_dotenv

from langchain.tools import tool


def init():
    load_dotenv(override=True)

@tool
def get_coordinates(place: str):
    """
    Retrieve the Google Places ID for a given place name located in Brussels.

    This function sends a text-based search query to the Google Places API,
    restricted to places in Brussels.

    Parameters
    ----------
    place : str
        The name of the place to search for (e.g., a landmark, building, or address).

    Returns
    -------
    str
        The Google Places ID of the first matching place.


    Notes
    -----
    - This function assumes the Google Places API endpoint
      `places:searchText` is available.
    - The search is biased by appending " brussels" to the query.
    """
    
    init()
    api_key = os.environ["GCLOUD_API_KEY"]

    params = {"key":api_key, "fields": "*"}
    payload = {"textQuery": place + " brussels"}
    place_details = requests.post("https://places.googleapis.com/v1/places:searchText", data=payload, params=params)
    place_json = place_details.json()
    
    place_id = place_json["places"][0]['id']

    return place_id

@tool
def get_route(origin: str, destination: str, departure_time:str):
    """
    Computes a public transit route between two locations using the Google Routes API.

    Args:
        origin (str): The Place ID of the starting location.
        destination (str): The Place ID of the destination location.
        departure_time (str): The desired departure time in RFC 3339 format
            (e.g., "2025-12-16T09:00:00Z").

    Returns:
        dict: A dictionary containing the route information returned by
            the Google Routes API. Typically includes routes, legs, steps, 
            and transit details.
    
    Example:
        >>> get_route("ChIJN1t_tDeuEmsRUsoyG83frY4", "ChIJLfySpTOuEmsRsc_JfJtljdc", "2025-12-16T09:00:00Z")
        {
            "routes": [
                ...
            ]
        }
    """
    api_key = os.environ["GCLOUD_API_KEY"]

    params = {"key": api_key, "fields": "routes"}
    payload = {
        "origin": {
            "placeId": origin
        }, 
        "destination": {
            "placeId":destination
        }, 
        "travelMode": "TRANSIT",
        #"transitPreferences": {
        #    "routingPreference": "LESS_WALKING"},
        "departureTime": departure_time,
        "languageCode": "en-US"
    }

    directions = requests.post("https://routes.googleapis.com/directions/v2:computeRoutes", json=payload, params=params).json()

    return directions


if __name__ == "__main__":
    print("gmaps tools module")
    #print(os.environ["GCLOUD_API_KEY"])
    flagey_coord = get_coordinates("Alma metro Station")
    midi = get_coordinates("gare du midi")

    itinerary = get_route(flagey_coord, midi, "2025-12-16T10:00:00Z")
    print(itinerary)
    with open("itinerary.json", "w") as f:
        f.write(json.dumps(itinerary))