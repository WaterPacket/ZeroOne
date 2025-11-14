from helper.getLiveScore import get_live_score
from helper.loadModel import load_model
from helper.predictor import predict_match_final_score
from helper.session_limits import session_limits

# Inputs
series = 'dummy_series'
match = 'dummy_match'
session = 'd'

#currentRuns, currentWicket, currentBallID, last_balls_string = get_live_score(series=series,match=match, session=session)
currentBallID = 51
currentRuns = 46
currentWicket = 2
last_balls_string = "4 4 0 6 1 4"

model, FEATURE_NAMES = load_model()

final_score_prediction = predict_match_final_score(
    currentBallID,
    currentRuns,
    currentWicket,
    last_balls_string,
    model,
    FEATURE_NAMES,
    session
)

print(f"🏏 Predicted Final T20 Score: {final_score_prediction}")

if isinstance(final_score_prediction, (int, float)):
    remaining_balls = session_limits.get(session) - currentBallID
    print(f"🧮 Need {final_score_prediction - currentRuns} runs in {remaining_balls} balls.")
