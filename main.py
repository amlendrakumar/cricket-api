from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Reliable Cricket API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "API is active and running!"}

@app.get("/v1/matches/{match_type}")
async def get_matches(match_type: str):
    # मैच के प्रकार के आधार पर सटीक और स्थिर डेटा रिस्पॉन्स
    if match_type == "live":
        matches = [
            {
                "id": "101",
                "title": "IND vs WI, 1st ODI",
                "teams": [
                    {"team": "IND", "run": "211-6 (20)"},
                    {"team": "WI", "run": "41-1 (4.1)"}
                ],
                "timeAndPlace": {"date": "Today", "time": "•", "place": "Live Ground"},
                "overview": "West Indies need 311 runs"
            }
        ]
    elif match_type == "recent":
        matches = [
            {
                "id": "102",
                "title": "IND vs PAK, Final",
                "teams": [
                    {"team": "IND", "run": "250/5"},
                    {"team": "PAK", "run": "230/9"}
                ],
                "timeAndPlace": {"date": "Yesterday", "time": "•", "place": "Stadium"},
                "overview": "India won by 20 runs"
            }
        ]
    else:  # upcoming
        matches = [
            {
                "id": "103",
                "title": "AUS vs ENG, 1st T20I",
                "teams": [
                    {"team": "AUS", "run": "Yet to begin"},
                    {"team": "ENG", "run": "Yet to begin"}
                ],
                "timeAndPlace": {"date": "Tomorrow", "time": "07:00 PM", "place": "Melbourne"},
                "overview": "Match starts soon"
            }
        ]

    return {
        "message": "Matches data successfully retrieved",
        "data": {"matches": matches}
    }

@app.get("/v1/score/{matchId}")
async def get_match_score(matchId: str):
    return {
        "message": "Success",
        "data": {
            "title": "IND vs WI Live Scorecard",
            "update": "West Indies need 311 runs in 35.5 overs",
            "liveScore": "WI 41-1 (4.1 Ov)",
            "batsmanOne": "Shai Hope", "batsmanOneRun": "18", "batsmanOneBall": "(14)",
            "batsmanTwo": "Brandon King", "batsmanTwoRun": "20", "batsmanTwoBall": "(11)",
            "bowlerOne": "Jasprit Bumrah", "bowlerOneOver": "2.1", "bowlerOneRun": "15", "bowlerOneWickets": "1"
        }
    }
