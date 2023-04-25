import requests 

# API URL
API_URL = 'https://statsapi.web.nhl.com/api/v1/'

# Get all scheduled playoff games
response = requests.get(API_URL + "schedule?season=20222023&gameType=P", params={"Content-Type": "application/json"})

# Convert JSON response to a dict
games = response.json()

# Traverse the 
game_links = []
for date in games['dates']:
    for game in date['games']:
        game_links.append(game['link'])

print(game_links)
    


