import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib
import os

def create_features(df):
    print("\n--- Starting Feature Engineering ---")

    # ── 1. Encode Binary Column (Gender) ────────────────────
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})
    print("✅ Encoded Gender")

    # ── 2. Label Encode Ordinal/Target Column (Test Results) ─
    # Normal=0, Inconclusive=1, Abnormal=2
    test_results_map = {'Normal': 0, 'Inconclusive': 1, 'Abnormal': 2}
    df['Test Results'] = df['Test Results'].map(test_results_map)
    print("✅ Encoded Test Results")

    # ── 3. One Hot Encode Categorical Columns ────────────────
    cat_cols = [
        'Blood Type',
        'Medical Condition',
        'Insurance Provider',
        'Admission Type',
        'Medication'
    ]
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)
    print(f"✅ One-hot encoded: {cat_cols}")

    # ── 4. Scale Numeric Columns ─────────────────────────────
    scaler = MinMaxScaler()
    numeric_cols = ['Age', 'Billing Amount', 'Length of Stay']
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    print(f"✅ Scaled numeric columns: {numeric_cols}")

    # ── 5. Save Scaler for Later Use ─────────────────────────
    os.makedirs('models', exist_ok=True)
    joblib.dump(scaler, 'models/scaler.pkl')
    print("✅ Saved scaler to models/scaler.pkl")

    # ── 6. Drop Date Columns (already used for Length of Stay)
    df = df.drop(columns=['Date of Admission', 'Discharge Date'])
    print("✅ Dropped date columns")

    print(f"\n--- Feature Engineering Complete: {df.shape[0]} rows, {df.shape[1]} columns ---")
    return df