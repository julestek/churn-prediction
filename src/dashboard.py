import streamlit as st
import requests

API_URL = "https://churn-prediction-2-t6c8.onrender.com/predict"

st.set_page_config(page_title="Prédiction Churn Client", page_icon="📊")

st.title("📊 Prédiction de Churn Client")
st.write("Renseignez les informations du client pour estimer son risque de départ.")

OUI_NON = ["Oui", "Non"]
OUI_NON_SANS_SERVICE = ["Oui", "Non", "Sans service internet"]

def to_yes_no(label):
    return "Yes" if label == "Oui" else "No"

def to_yes_no_service(label):
    mapping = {"Oui": "Yes", "Non": "No", "Sans service internet": "No internet service"}
    return mapping[label]

col1, col2 = st.columns(2)

with col1:
    gender_label = st.selectbox("Genre", ["Femme", "Homme"])
    gender = "Female" if gender_label == "Femme" else "Male"

    senior_label = st.selectbox("Client senior (65 ans et +)", OUI_NON)
    senior_citizen = 1 if senior_label == "Oui" else 0

    partner_label = st.selectbox("En couple", OUI_NON)
    partner = to_yes_no(partner_label)

    dependents_label = st.selectbox("Personnes à charge", OUI_NON)
    dependents = to_yes_no(dependents_label)

    tenure = st.slider("Ancienneté (mois)", 0, 72, 12,
                        help="Le modèle a été entraîné sur des clients ayant jusqu'à 72 mois d'ancienneté (6 ans)")

    phone_label = st.selectbox("Service téléphonique", OUI_NON)
    phone_service = to_yes_no(phone_label)

    multiple_lines_label = st.selectbox("Lignes multiples", ["Oui", "Non", "Sans service téléphonique"])
    multiple_lines = {"Oui": "Yes", "Non": "No", "Sans service téléphonique": "No phone service"}[multiple_lines_label]

    internet_label = st.selectbox("Service internet", ["DSL", "Fibre optique", "Aucun"])
    internet_service = {"DSL": "DSL", "Fibre optique": "Fiber optic", "Aucun": "No"}[internet_label]

    online_security_label = st.selectbox("Sécurité en ligne", OUI_NON_SANS_SERVICE)
    online_security = to_yes_no_service(online_security_label)

    online_backup_label = st.selectbox("Sauvegarde en ligne", OUI_NON_SANS_SERVICE)
    online_backup = to_yes_no_service(online_backup_label)

with col2:
    device_protection_label = st.selectbox("Protection appareil", OUI_NON_SANS_SERVICE)
    device_protection = to_yes_no_service(device_protection_label)

    tech_support_label = st.selectbox("Support technique", OUI_NON_SANS_SERVICE)
    tech_support = to_yes_no_service(tech_support_label)

    streaming_tv_label = st.selectbox("Streaming TV", OUI_NON_SANS_SERVICE)
    streaming_tv = to_yes_no_service(streaming_tv_label)

    streaming_movies_label = st.selectbox("Streaming Films", OUI_NON_SANS_SERVICE)
    streaming_movies = to_yes_no_service(streaming_movies_label)

    contract_label = st.selectbox("Type de contrat", ["Mensuel", "Un an", "Deux ans"])
    contract = {"Mensuel": "Month-to-month", "Un an": "One year", "Deux ans": "Two year"}[contract_label]

    paperless_label = st.selectbox("Facturation dématérialisée", OUI_NON)
    paperless_billing = to_yes_no(paperless_label)

    payment_label = st.selectbox("Méthode de paiement", [
        "Chèque électronique", "Chèque postal", "Virement automatique", "Carte bancaire automatique"
    ])
    payment_method = {
        "Chèque électronique": "Electronic check",
        "Chèque postal": "Mailed check",
        "Virement automatique": "Bank transfer (automatic)",
        "Carte bancaire automatique": "Credit card (automatic)"
    }[payment_label]

    monthly_charges = st.number_input("Facturation mensuelle (€)", 0.0, 200.0, 70.0)

    total_charges_estimated = monthly_charges * tenure
    total_charges = st.number_input(
        "Facturation totale (€)",
        0.0, 15000.0, float(total_charges_estimated),
        help="Calculé automatiquement (mensuel × ancienneté), mais ajustable si besoin"
    )

if st.button("🔍 Prédire le risque de churn"):
    client_data = {
        "gender": gender, "SeniorCitizen": senior_citizen, "Partner": partner,
        "Dependents": dependents, "tenure": tenure, "PhoneService": phone_service,
        "MultipleLines": multiple_lines, "InternetService": internet_service,
        "OnlineSecurity": online_security, "OnlineBackup": online_backup,
        "DeviceProtection": device_protection, "TechSupport": tech_support,
        "StreamingTV": streaming_tv, "StreamingMovies": streaming_movies,
        "Contract": contract, "PaperlessBilling": paperless_billing,
        "PaymentMethod": payment_method, "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }

    with st.spinner("Interrogation du modèle..."):
        response = requests.post(API_URL, json=client_data)

    if response.status_code == 200:
        result = response.json()
        probability = result["churn_probability"]
        prediction = result["churn_prediction"]

        st.divider()
        if prediction == 1:
            st.error(f"⚠️ Risque de churn élevé : {probability:.1%}")
        else:
            st.success(f"✅ Risque de churn faible : {probability:.1%}")

        st.progress(probability)
    else:
        st.error(f"Erreur API : {response.status_code}")