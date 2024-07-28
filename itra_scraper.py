import requests
from env import *

headers = {
    "User-Agent": USER_AGENT        
}

def get_json(url, request_type = "GET", form_data = {}):
    if request_type == "POST":
        r = requests.post(url, headers=headers, data=form_data)
    else:
        r = requests.get(url, headers=headers)
    return r.json()

def get_runners(start = 1, count = 100, gender = "", distance_id = 0, rating_min = 0, rating_max = 1000, age_group = "", continent_id = "", country_code = ""):
    url = "https://itra.run/api/runner/runnerrank"

    form_data = {
        "start": start,
        "count": count,
        "gender": gender,
        "distanceId": distance_id,
        "piStart": rating_min,
        "piEnd": rating_max,
        "age_group": age_group,
        "continentId": continent_id,
        "countryCode": country_code
    }

    return get_json(url, "POST", form_data)

