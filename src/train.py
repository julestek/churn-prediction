import joblib
import os
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier

from src.data_processing import load_data, clean_data, engineer_features, prepare_for_model


def train_model(data_path: str, model_output_path: str):
    """Entraîne le modèle final et le sauvegarde sur disque."""

    # 1. Chargement et préparation des données
    df = load_data(data_path)
    df = clean_data(df)
    df = engineer_features(df)
    df_model = prepare_for_model(df)

    X = df_model.drop(columns=['Churn_binary'])
    y = df_model['Churn_binary']

    # 2. Split train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Tuning XGBoost (mêmes paramètres que dans le notebook)
    ratio = (y_train == 0).sum() / (y_train == 1).sum()

    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 5, 7],
        'learning_rate': [0.01, 0.1, 0.2]
    }

    grid_search = GridSearchCV(
        estimator=XGBClassifier(scale_pos_weight=ratio, random_state=42, eval_metric='logloss'),
        param_grid=param_grid,
        scoring='f1',
        cv=3,
        n_jobs=-1
    )
    grid_search.fit(X_train, y_train)

    best_model = grid_search.best_estimator_

    # 4. Sauvegarde du modèle et des colonnes attendues
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(best_model, model_output_path)
    joblib.dump(list(X.columns), model_output_path.replace('.pkl', '_columns.pkl'))

    print(f"Modèle entraîné et sauvegardé : {model_output_path}")
    print(f"Meilleurs paramètres : {grid_search.best_params_}")


if __name__ == "__main__":
    train_model(
        data_path="data/WA_Fn-UseC_-Telco-Customer-Churn.csv",
        model_output_path="models/xgboost_churn_model.pkl"
    )