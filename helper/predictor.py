import pandas as pd
from helper.last_n_stats import calculate_last_n_stats
from helper.session_limits import session_limits


def predict_match_final_score(currentBallID, currentRuns, currentWicket, last_balls_string, model, feature_names, session):
    TOTAL_BALLS_IN_T20 = 120

    session = session.lower().strip()[0]
    target_ball = session_limits.get(session, 120)

    # If overs for this session already completed
    if currentBallID >= target_ball:
        return "over completed"

    # If innings already over (all out or full 20 overs done)
    if currentBallID >= TOTAL_BALLS_IN_T20 or currentWicket >= 10:
        return currentRuns

    # 1️⃣ Derived features (state at current ball)
    balls_remaining = TOTAL_BALLS_IN_T20 - currentBallID
    wickets_remaining = 10 - currentWicket
    overs_played = currentBallID / 6.0
    current_run_rate = currentRuns / overs_played if overs_played > 0 else 0

    # 2️⃣ Momentum features
    runs_last_n_proj, wickets_last_n_proj = calculate_last_n_stats(last_balls_string)

    # 3️⃣ Predict full-innings final score
    input_data = pd.DataFrame({
        'ballCount': [currentBallID],
        'runs': [currentRuns],
        'wickets': [currentWicket],
        'balls_remaining': [balls_remaining],
        'wickets_remaining': [wickets_remaining],
        'current_run_rate': [current_run_rate],
        'runs_last_n': [runs_last_n_proj],
        'wickets_last_n': [wickets_last_n_proj]
    })[feature_names]

    predicted_full_score = model.predict(input_data)[0]

    # 4️⃣ Adjust prediction to session target (proportionally to balls)
    projected_session_score = (
            currentRuns + (predicted_full_score - currentRuns) * (target_ball - currentBallID) / (TOTAL_BALLS_IN_T20 - currentBallID)
    )

    return int(round(projected_session_score))
