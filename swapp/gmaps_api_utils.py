import requests

GEOCODE_PREFIX = "https://maps.googleapis.com/maps/api/geocode/json"


def get_coordinates(location):
    url = "%s?address=%s,%s,%s,%s" % (GEOCODE_PREFIX, location.street, location.city, location.region, location.country)
    url = url.replace(" ", "+")
    r = requests.get(url)
    results = r.json()["results"]
    return [r["geometry"]["location"] for r in results]

