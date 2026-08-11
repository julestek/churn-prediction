import pandas as pd
from src.data_processing import clean_data, engineer_features


def test_clean_data_converts_total_charges_to_numeric():
    df = pd.DataFrame({
        'TotalCharges': ['100.5', ' ', '200.0'],
        'Churn': ['Yes', 'No', 'Yes']
    })

    result = clean_data(df)

    assert result['TotalCharges'].dtype == 'float64'
    assert result['TotalCharges'].iloc[1] == 0


def test_clean_data_encodes_churn_correctly():
    df = pd.DataFrame({
        'TotalCharges': ['100.5', '200.0'],
        'Churn': ['Yes', 'No']
    })

    result = clean_data(df)

    assert result['Churn_binary'].iloc[0] == 1
    assert result['Churn_binary'].iloc[1] == 0


def test_engineer_features_counts_services_correctly():
    df = pd.DataFrame({
        'OnlineSecurity': ['Yes', 'No'],
        'OnlineBackup': ['Yes', 'No'],
        'DeviceProtection': ['No', 'No'],
        'TechSupport': ['Yes', 'No'],
        'StreamingTV': ['No', 'No'],
        'StreamingMovies': ['No', 'No'],
    })

    result = engineer_features(df)

    assert result['nb_services_souscrits'].iloc[0] == 3
    assert result['nb_services_souscrits'].iloc[1] == 0