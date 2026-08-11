# 📊 Churn Prediction — Pipeline ML End-to-End

Pipeline complet de prédiction du churn client (attrition), du nettoyage des données jusqu'au déploiement en production. Projet réalisé pour développer les compétences data science attendues en mission ESN (banque, assurance, télécom).

🔗 **Démo live** : [Dashboard](https://churn-prediction-jules.streamlit.app/) · [API (docs)](https://churn-prediction-2-t6c8.onrender.com/docs)

> ⚠️ Les deux services tournent sur des tiers gratuits : la première requête peut prendre 30-60s (réveil du service).

---

## 🎯 Contexte

Prédire quels clients d'un opérateur télécom sont susceptibles de résilier, à partir de leurs données démographiques, contractuelles et de consommation. Cas d'usage classique en mission data science ESN.

**Dataset** : [Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) (Kaggle, ~7000 clients)

## 🏗️ Architecture

```
┌─────────────────┐ ┌──────────────────┐ ┌───────────────┐
│ Streamlit Cloud │─────▶│ Render (API) │─────▶│ Modèle XGBoost │
│ (dashboard) │ HTTP │ FastAPI │ │ (.pkl) │
└─────────────────┘ └──────────────────┘ └───────────────┘
```

## 🛠️ Stack technique

| Domaine | Outils |
|---|---|
| Manipulation de données | Python, pandas, SQL |
| Modélisation | scikit-learn, XGBoost |
| Tracking d'expériences | MLflow |
| Interprétabilité | SHAP |
| Tests | pytest |
| API | FastAPI, Uvicorn |
| Conteneurisation | Docker |
| CI/CD | GitHub Actions |
| Dashboard | Streamlit |
| Déploiement | Render (API), Streamlit Community Cloud (dashboard) |
| Gestion de dépendances | Poetry |

## 📈 Résultats

Comparaison de 5 modèles (métriques sur le test set) :

| Modèle | Accuracy | Precision | Recall | F1-score |
|---|---|---|---|---|
| Régression logistique (baseline) | 0.807 | 0.658 | 0.567 | 0.609 |
| Régression logistique (balanced) | 0.739 | 0.505 | 0.783 | 0.614 |
| Random Forest | 0.764 | 0.549 | 0.634 | 0.588 |
| XGBoost (défaut) | 0.771 | 0.559 | 0.647 | 0.600 |
| **XGBoost (tuné, GridSearchCV)** | **0.730** | 0.494 | **0.813** | **0.615** |

**Modèle retenu** : XGBoost tuné, meilleur recall et F1-score, priorisés car rater un client qui churne coûte plus cher qu'une fausse alerte.

**Facteurs de risque principaux** (analyse SHAP) : absence de contrat longue durée, faible ancienneté, fibre optique, paiement par chèque électronique.

## 🚀 Lancer le projet en local

### Prérequis
- Python 3.12 (recommandé via [pyenv](https://github.com/pyenv/pyenv))
- [Poetry](https://python-poetry.org/)
- Docker (optionnel, pour la conteneurisation)

### Installation

```bash
git clone https://github.com/julestek/churn-prediction.git
cd churn-prediction
poetry install
```

### Entraîner le modèle

```bash
poetry run python -m src.train
```

### Lancer l'API

```bash
poetry run uvicorn src.api:app --reload
```
Documentation interactive : http://localhost:8000/docs

### Lancer le dashboard

```bash
poetry run streamlit run src/dashboard.py
```

### Lancer avec Docker

```bash
docker build -t churn-prediction-api .
docker run -p 8000:8000 churn-prediction-api
```

### Lancer les tests

```bash
poetry run pytest
```

## 📁 Structure du projet

```
churn-project/
├── .github/workflows/     # CI/CD (tests automatiques)
├── notebooks/              # EDA, expérimentation, MLflow
├── src/
│   ├── data_processing.py  # Nettoyage et feature engineering
│   ├── train.py             # Entraînement et sauvegarde du modèle
│   ├── predict.py           # Logique de prédiction
│   ├── api.py                # API FastAPI
│   └── dashboard.py          # Dashboard Streamlit
├── tests/                   # Tests unitaires (pytest)
├── Dockerfile
└── pyproject.toml
```

## 🔄 CI/CD

Chaque push sur `main` déclenche automatiquement (GitHub Actions) :
1. Installation des dépendances
2. Téléchargement du dataset (Kaggle API)
3. Entraînement du modèle
4. Exécution des tests unitaires

## 📝 Méthodologie

1. **EDA** : analyse exploratoire, détection de valeurs manquantes déguisées, corrélations
2. **Feature engineering** : encodage one-hot, création de variables dérivées
3. **Modélisation** : comparaison de 5 modèles, gestion du déséquilibre de classes, tuning par cross-validation
4. **Interprétabilité** : analyse SHAP pour identifier les facteurs de risque actionnables
5. **Industrialisation** : code modulaire, tests, API, conteneurisation, CI/CD
6. **Déploiement** : API et dashboard accessibles publiquement

## Auteur

Jules  -- Étudiant ingénieur, spécialisation IA & Optimisation
