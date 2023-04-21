import requests
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to Atlas
client = pymongo.MongoClient(os.getenv('MONGOCLIENT_URL'))
db = client.test

url = 'http://api.football-data.org/v4/competitions/PL/standings'
headers = {'X-Auth-Token': os.getenv('X_AUTH_TOKEN')}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # The request was successful
    data = response.json()
    standings = data['standings'][0]['table']
    for team in standings:
        name = team['team']['name']
        points = team['points']
        position = team['position']
        gd = team['goalDifference']
        playedGames = team['playedGames']
        form = team['form']
        goalsForCalc = int(team['goalsFor']) / int(team['playedGames'])
        goalsForPG = str(round(goalsForCalc,2))
        goalsAgCalc = int(team['goalsAgainst']) / int(team['playedGames'])
        goalsAgPG = str(round(goalsAgCalc,2))
        
        # Store the data in Atlas
        db.standings.insert_one({
            "name": name,
            "points": points,
            "position": position,
            "goal_difference": gd,
            "played_games": playedGames,
            "form": form,
            "goals_for_pg": goalsForPG,
            "goals_against_pg": goalsAgPG
        })
        
else:
    # The request was unsuccessful
    print(f'Request failed with status code {response.status_code}')