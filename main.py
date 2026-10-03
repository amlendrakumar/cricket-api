from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="CricketData Live API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "cbdf8f46-1f47-423d-8c80-9d1ab1e78e1f"

@app.get("/")
def home():
    return {"status": "CricketData API is active and running!"}

@app.get("/v1/matches/{match_type}")
async def get_matches(match_type: str):
    # CricketData.org का करेंट मैच एंडपॉइंट
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=15.0)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch data from CricketData")
            
            result = response.json()
            data_list = result.get("data", [])
            matches = []

            for m in data_list:
                match_id = m.get("id", "101")
                name = m.get("name", "Cricket Match")
                status = m.get("status", "Match status")
                match_type_info = m.get("matchType", "").lower()
                
                # टीमों के नाम और स्कोर
                team_info = m.get("teamInfo", [])
                teams = []
                for t in team_info:
                    teams.append({
                        "team": t.get("shortname", "TEAM"),
                        "run": "Live"
                    })
                
                if not teams:
                    teams = [{"team": "Team 1", "run": "---"}, {"team": "Team 2", "run": "---"}]

                score_list = m.get("score", [])
                score_summary = ""
                if score_list:
                    for s in score_list:
                        score_summary += f"{s.get('inning')}: {s.get('r')}/{s.get('w')} ({s.get('o')} Ov) | "
                else:
                    score_summary = status

                matches.append({
                    "id": match_id,
                    "title": name,
                    "teams": teams,
                    "timeAndPlace": {"date": m.get("date", "Today"), "time": "•", "place": m.get("venue", "Stadium")},
                    "overview": score_summary
                })

            if not matches:
                matches = [{
                    "id": "101",
                    "title": "No Matches Live Right Now",
                    "teams": [{"team": "IND", "run": "---"}, {"team": "AUS", "run": "---"}],
                    "timeAndPlace": {"date": "Today", "time": "•", "place": "Ground"},
                    "overview": "Check back later for upcoming matches"
                }]

            return {
                "message": "Success",
                "data": {"matches": matches}
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/score/{matchId}")
async def get_match_score(matchId: str):
    url = f"https://api.cricapi.com/v1/match_scorecard?apikey={API_KEY}&id={matchId}"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=15.0)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Scorecard not found")
            
            res_json = response.json().get("data", {})
            
            return {
                "message": "Success",
                "data": {
                    "title": res_json.get("name", "Match Scorecard"),
                    "update": res_json.get("status", "Match in progress"),
                    "liveScore": "Real-time Data Synced",
                    "batsmanOne": "Batsman Info", "batsmanOneRun": "-", "batsmanOneBall": "-",
                    "batsmanTwo": "Batsman Info", "batsmanTwoRun": "-", "batsmanTwoBall": "-",
                    "bowlerOne": "Bowler Info", "bowlerOneOver": "-", "bowlerOneRun": "-", "bowlerOneWickets": "-"
                }
            }
        except Exception as e:
            return {
                "message": "Success",
                "data": {
                    "title": "Match Scorecard",
                    "update": "Loading live scorecard...",
                    "liveScore": "Syncing...",
                    "batsmanOne": "Batsman", "batsmanOneRun": "0", "batsmanOneBall": "(0)",
                    "batsmanTwo": "Batsman", "batsmanTwoRun": "0", "batsmanTwoBall": "(0)",
                    "bowlerOne": "Bowler", "bowlerOneOver": "0", "bowlerOneRun": "0", "bowlerOneWickets": "0"
                }
            }
