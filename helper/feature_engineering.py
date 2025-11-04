import numpy as np
import pandas as pd

TOTAL_BALLS_IN_T20 = 120

def feature_engineer_data(df, n_balls=24):
    df = df.copy()
    final_scores = df.groupby('match_innings_id').agg(
        target_final_score=('runs', 'last')
    ).reset_index()

    df = pd.merge(df, final_scores, on='match_innings_id')

    # 1. Current State Features
    df['balls_remaining'] = TOTAL_BALLS_IN_T20 - df['ballCount']
    df['wickets_remaining'] = 10 - df['wickets']
    df['overs_completed'] = np.floor(df['ballCount'] / 6)
    df['current_run_rate'] = df['runs'] / (df['overs_completed'].replace(0, 1) + (df['ballCount'] % 6)/6) # Avoid div by zero

    # 2. Momentum Features (Runs/Wickets in the Last N Balls)
    # These are powerful predictors of the team's current batting tempo.

    # Calculate instant runs and wickets for rolling window
    df['instant_runs'] = df['runs'] - df.groupby('match_innings_id')['runs'].shift(1, fill_value=0)
    df['instant_wicket'] = df['wickets'] - df.groupby('match_innings_id')['wickets'].shift(1, fill_value=0)

    # Rolling sum of the last N_LAST_BALLS (e.g., 5 overs = 30 balls)
    df['runs_last_n'] = df.groupby('match_innings_id')['instant_runs'].rolling(
        window=n_balls, min_periods=1
    ).sum().reset_index(level=0, drop=True)

    df['wickets_last_n'] = df.groupby('match_innings_id')['instant_wicket'].rolling(
        window=n_balls, min_periods=1
    ).sum().reset_index(level=0, drop=True)

    # Drop rows where wickets have already reached 10 (innings is over)
    df = df[df['ballCount'] <= 120]
    df = df[df['wickets'] < 10].reset_index(drop=True)

    # Select final features
    FEATURES = [
        'ballCount', 'runs', 'wickets', 'balls_remaining', 'wickets_remaining',
        'current_run_rate', 'runs_last_n', 'wickets_last_n'
    ]
    TARGET = 'target_final_score'

    return df[FEATURES + [TARGET]], FEATURES