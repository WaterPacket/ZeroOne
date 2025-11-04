import os

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from helper.feature_engineering import feature_engineer_data
from helper.load_data import load_all_innings_data

MODEL_PATH = "models/final_rf_model.pkl"
FEATURES_PATH = "models/feature_names.pkl"

def load_model():

    os.makedirs("models", exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print("📦 Existing model found — loading...")
        model = joblib.load(MODEL_PATH)
        FEATURE_NAMES = joblib.load(FEATURES_PATH)
        print("✅ Model loaded successfully.\n")
    else:
        print("🚀 No saved model found — training new model...")
        df_raw = load_all_innings_data()
        df_processed, FEATURE_NAMES = feature_engineer_data(df_raw)
        print("Data Processing Complete. Sample Features:")
        print(df_processed.head(5))
        print("-" * 50)

        X = df_processed[FEATURE_NAMES]
        y = df_processed['target_final_score']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print(f"Training data size: {len(X_train)}")

        model = RandomForestRegressor(n_estimators=500, max_depth=10, random_state=42, n_jobs=-1)
        model.fit(X_train, y_train)

        # Evaluate
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        print(f"✅ Model Trained Successfully. MAE on Test Set: {mae:.2f} runs")
        print("-" * 50)

        # Save model + features
        joblib.dump(model, MODEL_PATH)
        joblib.dump(FEATURE_NAMES, FEATURES_PATH)
        print(f"💾 Model and features saved to 'models/' directory.\n")

    return model, FEATURE_NAMES