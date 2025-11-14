# main.py
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from helper.loadModel import load_model
from helper.predictor import predict_match_final_score

app = FastAPI(title="Score Prediction API", version="1.0")


class ApiRequest(BaseModel):
    currentRuns: int
    currentBallId: int
    currentWicket: int
    lastBalls: List[str]
    session: str


model, FEATURE_NAMES = load_model()


@app.get("/")
async def root():
    return {"message": "Ping from Score Prediction API"}


@app.post("/predictScore")
async def get_predicted_score(req: ApiRequest):
    print("📦 Incoming Request Body:", req)

    final_score_prediction = predict_match_final_score(
        currentBallID=req.currentBallId,
        currentRuns=req.currentRuns,
        currentWicket=req.currentWicket,
        last_balls_string=" ".join(req.lastBalls),
        model=model,
        feature_names=FEATURE_NAMES,
        session=req.session,
    )
    print("📦 Outgoing Predicted Score:", final_score_prediction)
    return {"predicted_score": final_score_prediction}
