import requests

hostname = "http://localhost:7777/"

def get_live_score(series, match, session):
    url = f"{hostname}/getMasterData/{series}/{match}/{session}"
    response = requests.get(url)
    match_data = response.json()['scorecard']

    current_score = match_data["team1"]["score"] if match_data.get("innings", 1) == 1 else match_data["team2"]["score"]
    runs_str, wickets_str = current_score.split("/")

    return int(runs_str), int(wickets_str), match_data.get("ballId", 0), " ".join(match_data.get("lastBalls", []))