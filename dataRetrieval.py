import requests
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to Atlas
client = pymongo.MongoClient(os.getenv('MONGOCLIENT_URL'))
db = client.test

def insert_data(data):
    """Insert data into the database"""
    for team in data:
        db.standings.insert_one({
            "teamName": team['team']['name'],
            "teamPoints": team['points'],
            "teamPosition": team['position'],
            "teamGoalDifference": team['goalDifference'],
            "teamGamesPlayed": team['playedGames'],
            "teamForm": team['form'],
            "teamScoreAverage": str(round(int(team['goalsFor']) / int(team['playedGames']), 2)),
            "teamConcedeAverage": str(round(int(team['goalsAgainst']) / int(team['playedGames']), 2))
        })

url = 'http://api.football-data.org/v4/competitions/PL/standings'
headers = {'X-Auth-Token': os.getenv('X_AUTH_TOKEN')}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    # The request was successful
    data = response.json()
    standings = data['standings'][0]['table']
    db.standings.delete_many({})
    insert_data(standings)
        
else:
    # The request was unsuccessful
    print(f'Request failed with status code {response.status_code}')