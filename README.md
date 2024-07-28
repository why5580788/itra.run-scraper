# itra.run Scraper

## Using itra_scraper

Just import **itra_scraper** and call functions!


### Runners Scraping

```python
from itra_scraper import get_runners
print(get_runners())

[
    {
        'runnerId': 687094,
        'rank': 1,
        'pi': 956,
        'name': 'Remi BONNET',
        'firstName': 'Remi',
        'lastName': 'BONNET',
        'ageGroup': 'M 23-34', 
        'age': 0, 
        'profilePic': '/Files/Photos/pic15965_ea1561f3.jpg',
        'nationality': 'Switzerland',
        'countryCode': '/images/CountryFlags/ch.svg',
        'gender': 'H'
    }, ...
]
```

#### Parameters:

| Key       | Type       | Default     | Description                                                      |
|-----------|------------|-------------|-----------------------------------------------------|
| start        | integer | 1 | The starting index of the results. |
| count        | integer | 100 | The number of results to retrieve.                                                  |
| gender       | string  | | The gender of the runners ("H" for male, "F" for female, "" for all).  |
| distance_id  | integer | 0 |The distance ID for filtering the runners. 0 = All, 1 = Vertical, 2 = 10K, 3 = Half Marathon, 4 = Marathon, 5 = 50k, 6 = 50M, 7 = 100K, 8 = 100M, 9 = Endurance. |
| rating_min   | integer | 0 |  The minimum "Performance Index" of the runners.                        |
| rating_max   | integer | 1000 | The maximum "Performance Index" of the runners.                     |
| age_group    | string  | | The age group of the runners. "" = Overall, M U18, F U18, M U20, F U20, M U23, F U23, M 23-34, F 23-34, M 35-39, F 35-39, M 40-44, F 40-44, M 45-49, F 45-49, M 50-54, F 50-54, M 55-59, F 55-59, M 60-64, F 60-64, M 65-69, F 65-69, M 70-74, F 70-74, M 75-79, F 75-79, M 80+, F 80+. |
| continent_id | integer | | The continent ID for filtering the runners. "" = World, 1 = Africa, 2 = North America, 3 = South America, 4 = Asia, 5 = Europe, 6 = Oceania, 99 = Other |
| country_code | string  | | The country code for filtering the runners.|


### Runner Scraping

```python
from itra_scraper import get_runner
print(get_runner(id = "687094"))

{
    'name': 'Remi BONNET',
    'performance_index': 956,
    'country': 'Switzerland',
    'age_group': 'M 23-34',
    'age': 29,
    'club': 'Salomon',
    'sponsor': 'Salomon | RedBull',
    'best_race_score': 970,
    'races_finished': '36/39',
    'world_ranking_percentage': 100.0,
    'world_ranking': '1 / 2 993 150',
    'continent_ranking': '1 / 1 833 058',
    'country_ranking': '1 / 66 388',
    'age_group_world_ranking': '1 / 388 149',
    'age_group_continent_ranking': '1 / 244 566',
    'age_group_country_ranking': '1 / 7 713'
}
```

#### Parameters:

| Key       | Type       | Default     | Description                                                      |
|-----------|------------|-------------|-----------------------------------------------------|
| id        | string |  | Runner ITRA ID |