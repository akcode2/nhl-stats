import requests 

from cs50 import SQL

# Connect database using CS50 library
db = SQL('sqlite:///playoffs.db')

# API URL
API_URL = 'https://statsapi.web.nhl.com'

# Get all scheduled playoff games and convert JSON response to a dict
response = requests.get(API_URL + "/api/v1/schedule?season=20222023&gameType=P", params={"Content-Type": "application/json"}).json()


# Traverse the lists and dicts to get the game links
game_links = []
for date in response['dates']:
    for game in date['games']:
        game_links.append(game['link'])

series = {}

for link in game_links:
    link_response = requests.get(API_URL + link).json()
    away_team = link_response['gameData']['teams']['away']['name']
    home_team = link_response['gameData']['teams']['home']['name']
    name_variants = [f'{away_team} v {home_team}', f'{home_team} v {away_team}']

    # If a key for this series already exists
    if name_variants[0] in series:
            # Get that series's keys - which are 'Game 1', 'Game 2', etc.
            # and extract just the number
            game_numbers = [int(key.split('_')[1]) for key in series[name_variants[0]].keys()]
            # Determine the highest number
            highest_game_number = max(game_numbers)
            # Then append link_response as the value of the next Game, which is itself a dict
            series[name_variants[0]][f'Game_{highest_game_number + 1}'] = link_response
    elif name_variants[1] in series:
            # Get that series's keys - which are 'Game 1', 'Game 2', etc.
            # and extract just the number
            # game_numbers = [int(key.split('_')[1]) for key in series[name_variants[1]].keys()]
            game_numbers = [int(key.split('_')[1]) for key in series[name_variants[1]].keys()]
            # Determine the highest number
            highest_game_number = max(game_numbers)
            # Then append link_response as the value of the next Game, which is itself a dict
            series[name_variants[1]][f'Game_{highest_game_number + 1}'] = link_response
    else:
            # Create the key for this series and assign it's value to a dict named Game_1
            series[f'{name_variants[0]}'] = dict(Game_1 = link_response)


for matchup in series:
      for game in series[matchup]:
        # Get a list of the scoring plays
        scoring_plays = series[matchup][game]['liveData']['plays']['scoringPlays']

        # Make a dict to store the data that we really want
        scoringPlays = {}
        for play in scoring_plays:
                period = series[matchup][game]['liveData']['plays']['allPlays'][play]['about']['period']
                period_time = series[matchup][game]['liveData']['plays']['allPlays'][play]['about']['periodTime']
                scoring_team = series[matchup][game]['liveData']['plays']['allPlays'][play]['team']['name']

                play_number = str(scoring_plays.index(play))
                
                # Append data to scoringPlays dict
                scoringPlays.update( {
                      f'{play_number}' : {
                        "period" : period,
                        "period_time" : period_time,
                        "scoring_team" : scoring_team
                      }
                })
        # Add the dict as a new key for the game
        series[matchup][game]['scoringPlays'] = scoringPlays


# Insert all the plays into playoffs.db
for matchup in series:
      for game in series[matchup]:
            db.execute("INSERT INTO scoring_plays (matchup, game_number, datetime, period, period_time, scoring_team)) VALUES (?, ?, ?, ?, ?, ?)",
                        )


CREATE TABLE scoring_plays (
    play_id INTEGER PRIMARY KEY,
    matchup TEXT NOT NULL,
    game_number INTEGER NOT NULL,
    datetime DATETIME, 
    period INTEGER, 
    period_time TIME, 
    scoring_team TEXT NOT NULL
    );

# for matchup in series:
#       print(matchup)

# print(series['New York Islanders v Carolina Hurricanes']['Game_1']['scoringPlays'])
            





