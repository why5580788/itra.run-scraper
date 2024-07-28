import requests
from bs4 import BeautifulSoup
from env import *

headers = {
    "User-Agent": USER_AGENT        
}

def get_request(url, request_type = "GET", response_type = "text", form_data = {}):
    if request_type == "POST":
        r = requests.post(url, headers=headers, data=form_data)
    else:
        r = requests.get(url, headers=headers)

    if response_type == "json":
        return r.json()
    
    return BeautifulSoup(r.content, 'html.parser') 

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

    return get_request(url, "POST", "json", form_data)

def get_runner(id):
    url = f"https://itra.run/RunnerSpace/{id}"

    soup = get_request(url)
    runner = {}

    runner['name'] = soup.select_one(".runner-name h1").text.strip()
    runner['performance_index'] = int(soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(1) > div > div.col.col-md-6 > div:nth-child(1) > div.col-lg-4.d-flex.align-items-start > span > small").text.split(" | ")[-1].strip())
    runner['country'] = soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(1) > div > div.col.col-md-6 > div.row.mt-3 > div > div > div:nth-child(1) > div > span").text.strip()
    runner['age_group'] = soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(1) > div > div.col.col-md-6 > div.row.mt-3 > div > div > div:nth-child(2) > div > span").text.strip()
    runner['age'] = int(soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(1) > div > div.col.col-md-6 > div.row.mt-3 > div > div > div:nth-child(3) > div > span").text.strip())
    try:
        runner['club'] = soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(1) > div > div.col.col-md-6 > div.row.mt-3 > div > div > div:nth-child(4) > div > span").text.strip()
    except:
        runner['club'] = ""
    try:
        runner['sponsor'] = soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(1) > div > div.col.col-md-6 > div.row.mt-3 > div > div > div:nth-child(5) > div > span").text.strip().replace("\n", "| ")
    except:
        runner['sponsor'] = ""
    runner['best_race_score'] = int(soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div > div > table > tbody > tr:nth-child(2) > td:nth-child(2)").text)
    runner['races_finished'] = soup.select_one("body > div:nth-child(2) > div > main > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div > div > table > tbody > tr:nth-child(3) > td:nth-child(2)").text.strip()

    runner_ranking = get_request("https://itra.run/api/Runner/RefreshRunnerPiGeneralStats", "POST", "json", {"runnerId": id})

    runner['world_ranking_percentage'] = float(runner_ranking["worldRankingPercentage"])
    runner['world_ranking'] = runner_ranking["worldRanking"]
    runner['continent_ranking'] = runner_ranking["continentRanking"]
    runner['country_ranking'] = runner_ranking["countryRanking"]
    runner['age_group_world_ranking'] = runner_ranking["ageGroupWorldRanking"]
    runner['age_group_continent_ranking'] = runner_ranking["ageGroupContinentRanking"]
    runner['age_group_country_ranking'] = runner_ranking["ageGroupCountryRanking"]

    return runner
