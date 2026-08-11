from src.predict import preprocess_input, expected_columns


def test_preprocess_input_returns_expected_columns():
    client_data = {
        "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
        "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
        "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
        "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
        "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check", "MonthlyCharges": 70.5, "TotalCharges": 846.0
    }

    result = preprocess_input(client_data)

    assert list(result.columns) == expected_columns
    assert result.shape[0] == 1