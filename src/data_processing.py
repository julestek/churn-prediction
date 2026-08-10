import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """Charge le dataset brut depuis un fichier CSV."""
    return pd.read_csv(filepath)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie le dataset : corrige TotalCharges, encode Churn."""
    df = df.copy()
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    df['Churn_binary'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les features dérivées (nombre de services souscrits)."""
    df = df.copy()
    services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
                'TechSupport', 'StreamingTV', 'StreamingMovies']
    df['nb_services_souscrits'] = (df[services] == 'Yes').sum(axis=1)
    return df


def prepare_for_model(df: pd.DataFrame) -> pd.DataFrame:
    """Encode les variables catégorielles pour la modélisation."""
    df_model = df.drop(columns=['customerID', 'Churn'])
    df_model = pd.get_dummies(df_model, drop_first=True)
    return df_model