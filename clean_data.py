import pandas as pd

def clean_data(df):
    print("\n--- Starting Data Cleaning ---")

    # ── 1. Fix name casing ──────────────────────────────────
    df['Name'] = df['Name'].str.title()
    print("✅ Fixed name casing")

    # ── 2. Parse dates ──────────────────────────────────────
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    print("✅ Parsed date columns")

    # ── 3. Engineer length of stay ──────────────────────────
    df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
    print("✅ Created Length of Stay column")

    # ── 4. Clip negative billing amounts ────────────────────
    df['Billing Amount'] = df['Billing Amount'].clip(lower=0)
    print("✅ Clipped negative billing amounts")

    # ── 5. Drop high cardinality / useless columns ──────────
    df = df.drop(columns=['Name', 'Doctor', 'Hospital', 'Room Number'])
    print("✅ Dropped high cardinality columns")

    # ── 6. Strip whitespace from string columns ─────────────
    str_cols = df.select_dtypes(include='object').columns
    df[str_cols] = df[str_cols].apply(lambda x: x.str.strip())
    print("✅ Stripped whitespace from string columns")

    # ── 7. Check for nulls ──────────────────────────────────
    nulls = df.isnull().sum()
    if nulls.any():
        print(f"⚠️ Nulls found:\n{nulls[nulls > 0]}")
    else:
        print("✅ No null values found")

    print(f"\n--- Cleaning Complete: {df.shape[0]} rows, {df.shape[1]} columns ---")
    return df