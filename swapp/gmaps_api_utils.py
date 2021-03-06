from math import sin, cos, sqrt, asin, radians, pi

import requests

GEOCODE_PREFIX = "https://maps.googleapis.com/maps/api/geocode/json"
EARTH_RADIUS = 6371  # km
MAX_RADIUS = pi * EARTH_RADIUS


class OverQueryLimitError(Exception):
    pass


def get_coordinates(location):
    print("[INFO] call to google maps API")
    url = "%s?address=%s,%s,%s,%s" % (GEOCODE_PREFIX, location.street, location.city, location.region, location.country)
    url = url.replace(" ", "+")
    r = requests.get(url)
    results = r.json()["results"]

    if r.json()["status"] == "OVER_QUERY_LIMIT":
        raise OverQueryLimitError()

    return [r["geometry"]["location"] for r in results]


def compute_distance(lat1, lon1, lat2, lon2):
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lon1, lat2, lon2))

    lat = lat2 - lat1
    lon = lng2 - lng1
    a = sin(lat/2) ** 2 + cos(lat1) * cos(lat2) * sin(lon/2) ** 2

    return 2 * EARTH_RADIUS * asin(sqrt(a))
