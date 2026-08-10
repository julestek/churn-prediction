import pandas as pd
import joblib

MODEL_PATH = "models/xgboost_churn_model.pkl"
COLUMNS_PATH = "models/xgboost_churn_model_columns.pkl"

model = joblib.load(MODEL_PATH)
expected_columns = joblib.load(COLUMNS_PATH)


def preprocess_input(client_data: dict) -> pd.DataFrame:
    """Transforme les données brutes d'un client en format attendu par le modèle."""
    df = pd.DataFrame([client_data])

    services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['nb_services_souscrits'] = (df[services] == 'Yes').sum(axis=1)

    df = pd.get_dummies(df)

    df = df.reindex(columns=expected_columns, fill_value=0)

    return df


def predict_churn(client_data: dict) -> dict:
    """Prédit la probabilité de churn pour un client donné."""
    X = preprocess_input(client_data)

    probability = model.predict_proba(X)[0][1]
    prediction = int(probability >= 0.5)

    return {
        "churn_prediction": prediction,
        "churn_probability": round(float(probability), 4)
    }