import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

# Load clinical data
clinical_df = pd.read_csv('COVID_NY_SBU_clinical.csv')

# Create outcomes
clinical_df['icu_admission'] = clinical_df['is_icu'].astype(int)
clinical_df['mechanical_ventilation'] = (clinical_df['was_ventilated'] == 'Yes').astype(int)
clinical_df['death'] = (clinical_df['last.status'] == 'deceased').astype(int)

# Load radiomics features
radiomics_df = pd.read_csv('fast_covid_analysis.csv')

# Merge patient data
merged = radiomics_df.merge(
    clinical_df[['to_patient_id', 'icu_admission', 'mechanical_ventilation', 'death']],
    left_on='patient_id',
    right_on='to_patient_id',
    how='inner'
)

features = ['covid_risk_score', 'lung_volume', 'ground_glass_opacity']
X = merged[features].fillna(0)

outcomes = ['icu_admission', 'mechanical_ventilation', 'death']
predictions = merged.copy()

for outcome in outcomes:
    y = merged[outcome]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
    print(f"{outcome} AUC: {auc:.3f}")

    predictions[f'{outcome}_probability'] = model.predict_proba(X)[:, 1]

# Save to CSV
predictions.to_csv('/app/results/complete_covid_triage_all_predictions.csv', index=False)
print('Saved all predictions to complete_covid_triage_all_predictions.csv')
