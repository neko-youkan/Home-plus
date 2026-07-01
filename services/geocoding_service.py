import requests


def search_location(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
        "format": "json",
        "limit": 1,
        "countrycodes": "jp",
    }

    headers = {
        "User-Agent": "HomePlusApp/1.0"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    result = data[0]

    return {
        "name": result.get("display_name", address),
        "lat": result["lat"],
        "lon": result["lon"],
    }