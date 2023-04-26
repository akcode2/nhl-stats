# nhl-stats
Using the NHL API and Python to analyze when goals were scored in the 22-23 NHL Playoffs

# Log
The URL for the NHL stats API is https://statsapi.web.nhl.com/api/v1/. There is no public documentation for it, but the wonderful [Drew Hynes](https://gitlab.com/dword4/nhlapi) has done a great job documenting it.

I used the [requests](https://requests.readthedocs.io/en/latest/) library for Python to interact with the API.

---
## Gathering the links
I began by retrieving the links in the API to all the playoff games and decoding the JSON response into a Python dict.

`response = requests.get(API_URL + "schedule?season=20222023&gameType=P", params={"Content-Type": "application/json"}).json()`

I stored these links in a list called `game_links`.
```for date in response['dates']:
    for game in date['games']:
        game_links.append(game['link'])
```
## Fetching every game as data
The amount of information provided for each game amounts to a full picture of the game in the form of data. I was mainly concerned with the scoring plays, but I stored every game in a dictionary called `series` so that this code can be easily updated in the future to answer different questions like "Which player receives the most penalties in the second period?". 

I decided to store the games by matchup, for example:
```
for link in game_links:
    link_response = requests.get(API_URL + link).json()
    ...
    series['New York Islanders v Carolina Hurricanes'][Game_1] = link_response
```
## Storing the data in a SQLite database
Rather than querying the API for all the games every time I wanted to analyze it, I stored everything in a SQLite database.
The schema of the database is:
```
CREATE TABLE scoring_plays (
    play_id INTEGER PRIMARY KEY,
    matchup TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    datetime DATETIME, 
    period INTEGER, 
    period_time TIME, 
    scoring_team TEXT NOT NULL
    );
```

I used the SQLAlchemy library for Python to connect to the database.
