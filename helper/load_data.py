import glob
import os
import pandas as pd

def load_all_innings_data():
    all_files = glob.glob("data/**/*.csv", recursive=True)
    df_list = []
    for file_path in all_files:
        try:
            df = pd.read_csv(file_path)
            unique_id = os.path.splitext(file_path)[0].replace('/', '_').replace('\\', '_')
            df['match_innings_id'] = unique_id
            if 'ballCount' not in df.columns or 'runs' not in df.columns or 'wickets' not in df.columns:
                print(f"Skipping {file_path}: Missing required columns (ballCount, runs, wickets).")
                continue

            df_list.append(df)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    if not df_list:
        return pd.DataFrame(columns=['ballCount', 'runs', 'wickets', 'match_innings_id', 'runs_on_ball', 'wicket_on_ball'])

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df['runs_on_ball'] = combined_df['runs'].diff().fillna(combined_df['runs'])
    combined_df['wicket_on_ball'] = combined_df['wickets'].diff().fillna(combined_df['wickets'])

    print("Data loading completed successfully.")
    print(f"Total Innings Loaded: {combined_df['match_innings_id'].nunique()}")
    print(f"Total Balls Found : {len(combined_df)}")
    return combined_df