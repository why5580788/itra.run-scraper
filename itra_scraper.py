import requests
from bs4 import BeautifulSoup
from env import *

headers = {
    "User-Agent": USER_AGENT,
    "Cookie": COOKIE        
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

    return get_request(RUNNERS_URL, "POST", "json", form_data)

def get_runner(id):
    url = f"{RUNNER_ABOUT_URL}{id}"

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

    runner_ranking = get_request(RUNNER_PI_STATS_URL, "POST", "json", {"runnerId": id})

    runner['world_ranking_percentage'] = float(runner_ranking["worldRankingPercentage"])
    runner['world_ranking'] = runner_ranking["worldRanking"]
    runner['continent_ranking'] = runner_ranking["continentRanking"]
    runner['country_ranking'] = runner_ranking["countryRanking"]
    runner['age_group_world_ranking'] = runner_ranking["ageGroupWorldRanking"]
    runner['age_group_continent_ranking'] = runner_ranking["ageGroupContinentRanking"]
    runner['age_group_country_ranking'] = runner_ranking["ageGroupCountryRanking"]

    runner['results'] = []
    results_url = f"{RUNNER_RACE_RESULTS_URL}{id}"
    soup = get_request(results_url)

    for year in soup.select("#runner-results-table"):
        for result in year.select("tbody tr"):
            result_data = {}
            row = result.select("td")
            result_data['date'] = row[0].text.strip()
            result_data['name_of_the_race'] = row[1].text.strip()
            result_data['race_id'] = row[1].find("a")['href'].split("/")[-1]
            result_data['country'] = row[2].text.strip()
            distance_text, elevation_gain_text = row[3].text.split("/")
            result_data['distance'] = int(distance_text.replace("km", "").strip())
            result_data['elevation_gain'] = int(elevation_gain_text.replace("m+", "").strip())
            result_data['time'] = row[4].text.strip()
            result_data['ranking'] = row[5].text.strip()
            result_data['ranking_gender'] = row[6].text.strip()
            result_data['race_score'] = row[7].text.strip()

            runner['results'].append(result_data)

    return runner

def get_race(id):
    url = f"{RACE_DETAILS_URL}{id}"

    soup = get_request(url)
    race = {}

    race['event_name'] = soup.select_one("body > div:nth-child(2) > div.discover-trail-running > div > div > div > div > div > div:nth-child(2) > div.col-lg-7 > h1").text.strip()

    race['race_name'] = soup.select_one("body > div:nth-child(2) > div.container.border.border-dark.mb-4 > div:nth-child(2) > div.col-lg-5 > div:nth-child(2) > div > h3").text.strip()
    race['itra_points'] = int(soup.select_one("body > div:nth-child(2) > div.container.border.border-dark.mb-4 > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2) > div > img")['alt'].strip())
    race['mountain_level'] = int(soup.select_one("body > div:nth-child(2) > div.container.border.border-dark.mb-4 > div:nth-child(2) > div:nth-child(3) > div > div:nth-child(2) > div > div > span:nth-child(2)").text.strip())
    race['finisher_level'] = int(soup.select_one("body > div:nth-child(2) > div.container.border.border-dark.mb-4 > div:nth-child(2) > div:nth-child(4) > div > div:nth-child(2) > div > div > span:nth-child(2)").text.strip())

    race['date'] = soup.select_one("#rdetails > div:nth-child(2) > div:nth-child(1) > span").text.replace("/", "-").strip()
    race['start_time'] = soup.select_one("#rdetails > div:nth-child(2) > div:nth-child(2) > span").text.strip()
    race['participation'] = soup.select_one("#rdetails > div:nth-child(2) > div:nth-child(3) > span").text.strip()

    race['distance'] = float(soup.select_one("#rdetails > div:nth-child(3) > div:nth-child(1) > span").text.strip())
    race['elevation_gain'] = int(soup.select_one("#rdetails > div:nth-child(3) > div:nth-child(2) > span").text.replace("+", "").strip())
    race['elevation_loss'] = int(soup.select_one("#rdetails > div:nth-child(3) > div:nth-child(3) > span").text.replace("-", "").strip())

    race['time_limit'] = soup.select_one("#rdetails > div:nth-child(4) > div:nth-child(1) > span").text.strip()
    race['number_of_aid_stations'] = int(soup.select_one("#rdetails > div:nth-child(4) > div:nth-child(2) > span").text.strip())
    race['number_of_participants'] = int(soup.select_one("#rdetails > div:nth-child(4) > div:nth-child(3) > span").text.strip())

    race["about_the_race"] = soup.select_one("#rdetails > div:nth-child(7) > div").text.replace("\n", " ").strip()

    url = f"{RACE_COURSE_URL}{id}"
    soup = get_request(url)

    race["start_location"] = soup.select_one("#rresults > div:nth-child(2) > div:nth-child(1) > h4").text.replace("Start Location:", "").strip()
    race["finish_location"] = soup.select_one("#rresults > div:nth-child(2) > div:nth-child(2) > h4").text.replace("Finish Location:", "").strip()
    race["type_of_terrain"] = soup.select_one("#rresults > div:nth-child(3) > div > h4").text.replace("Type of Terrain:", "").strip()
    race["trace_de_trail_url"] = soup.select_one("#rresults div.race-course-btn > a")['href']

    url = f"{RACE_RESULTS_URL}{id}"
    soup = get_request(url)
    race["results"] = []

    has_subscription = True

    for row in soup.select("#RunnerRaceResults > tr"):
        result = {}
        td = row.select("td")

        result['place'] = td[0].text.strip()
        result['name'] = td[1].text.strip()
        result['runner_id'] = td[1].find("a")["href"].split("/")[-1]
        result['time'] = td[2].text.strip()

        if (has_subscription):
            result['race_score'] = td[3].text.strip()
            try:
                result['age'] = int(td[4].text.strip())
            except:
                result['age'] = None
            result['gender'] = td[5].text.strip()
            result['nationality'] = td[6].text.strip()
        else:
            result['race_score'] = "Subscription is needed"
            try:
                result['age'] = int(td[3].text.strip())
            except:
                result['age'] = None
            result['gender'] = td[4].text.strip()
            result['nationality'] = td[5].text.strip()

        if len(td[3].select(".itra-green-bgr")) > 0:
            has_subscription = False
            result['race_score'] = "Subscription is needed"

        race["results"].append(result)

    return race
