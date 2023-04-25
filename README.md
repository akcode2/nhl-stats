# nhl-stats
Using the NHL API and Python to analyze when goals were scored in the 22-23 NHL Playoffs

# Log
The URL for the NHL stats API is https://statsapi.web.nhl.com/api/v1/. There is no public documentation for it, but the wonderful [Drew Hynes](https://gitlab.com/dword4/nhlapi) has done a great job documenting it.

I used the [requests](https://requests.readthedocs.io/en/latest/) library for Python to interact with the API. 

I passed in the query `schedule?season=20222023&gameType=P` to get all the playoff games in the 22-23 season.

`response = requests.get(API_URL + "schedule?season=20222023&gameType=P", params={"Content-Type": "application/json"})`

I decoded the JSON into a Python dict, `games=response.json()`. 

I made a list called `game_links` and populated it with the game links which are contained within nested links and dicts.

```for date in games['dates']:
    for game in date['games']:
        game_links.append(game['link'])
```