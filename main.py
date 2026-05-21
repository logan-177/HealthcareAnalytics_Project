import sqlite3
import pandas as pd
import os
from pathlib import Path
from src.load_data import load
from src.clean_data import clean_data
from src.features import create_features

DB_PATH = Path(__file__).resolve().parent / 'data' / 'healthcare.db'
CSV_PATH = Path(__file__).resolve().parent / 'data' / 'raw' / 'healthcare_dataset.csv'

def setup_database():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        df_raw = pd.read_csv(CSV_PATH)
        df_raw.to_sql('patients', conn, if_exists='replace', index=False)
        conn.commit()   # ← add this
        conn.close()
        print("✅ Database created from healthcare_dataset.csv")
    else:
        print("✅ Database already exists, skipping setup")

def main():
    print("\n=== Starting Healthcare Data Pipeline ===\n")

    # 1. Setup database (one-time)
    setup_database()
        # TEST - add these 3 lines
    import src.load_data as ld
    print(f"🔍 DB_PATH in load_data: {ld.DB_PATH}")
    print(f"🔍 File exists: {ld.DB_PATH.exists()}")
    
    df = load()
    # 2. Load data from SQLite
    df = load()
    print(f"✅ Loaded data shape: {df.shape}")

    # 3. Clean data
    df_clean = clean_data(df)
    print(f"✅ After cleaning: {df_clean.shape}")

    # 4. Feature engineering
    df_features = create_features(df_clean)
    print(f"✅ Features created: {df_features.shape}")

    # 5. Save output
    output_path = Path("data/processed/processed_dataset.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_features.to_csv(output_path, index=False)
    print(f"✅ Saved processed data to: {output_path}")

    print("\n=== Pipeline Complete ===\n")

if __name__ == "__main__":
    main()