# Healthcare Data Pipeline

A modular Python data pipeline built on a synthetic healthcare dataset containing 55,500 patient records. The project simulates a real-world EMR (Electronic Medical Records) data workflow — from raw ingestion through cleaning, feature engineering, and preparation for predictive modeling.

---

## Project Structure

```
New_HealthcareProject/
│
├── main.py                        # Orchestrates the full pipeline
├── requirements.txt               # Project dependencies
│
├── data/
│   ├── raw/
│   │   └── healthcare_dataset.csv # Original raw data, never modified
│   ├── healthcare.db              # SQLite database (auto-generated)
│   └── processed/
│       └── processed_dataset.csv  # Final output after pipeline runs
│
├── models/
│   └── scaler.pkl                 # Saved MinMaxScaler for reuse
│
├── src/
│   ├── load_data.py               # Loads data from SQLite database
│   ├── clean_data.py              # Cleans and validates raw data
│   └── features.py                # Feature engineering and encoding
│
└── notebooks/
    └── eda.ipynb                  # Exploratory data analysis
```

---

## Dataset

The dataset is a synthetic EMR-style dataset with the following attributes:

| Column | Type | Description |
|---|---|---|
| Name | String | Patient name |
| Age | Numeric | Patient age (10–90) |
| Gender | Categorical | Male / Female |
| Blood Type | Categorical | A+, A-, B+, B-, O+, O-, AB+, AB- |
| Medical Condition | Categorical | Cancer, Obesity, Diabetes, etc. |
| Date of Admission | DateTime | Hospital admission date |
| Discharge Date | DateTime | Hospital discharge date |
| Doctor | String | Attending doctor |
| Hospital | String | Hospital name |
| Insurance Provider | Categorical | Blue Cross, Medicare, Aetna, etc. |
| Billing Amount | Numeric | Total billed amount |
| Room Number | Numeric | Assigned room number |
| Admission Type | Categorical | Urgent, Emergency, Elective |
| Medication | Categorical | Paracetamol, Ibuprofen, Aspirin, etc. |
| Test Results | Categorical | Normal, Inconclusive, Abnormal **(target)** |

---

## Pipeline Steps

### 1. Database Setup
The raw CSV is loaded into a local SQLite database on first run. Every subsequent run reads directly from the database, mirroring a real-world SQL workflow.

```python
# First run: builds the database
setup_database()

# Every run: queries via SQL
df = load("SELECT * FROM patients")
```

### 2. Data Cleaning (`src/clean_data.py`)
- Fixed inconsistent name casing (e.g. `BoBBy jACKsOn` → `Bobby Jackson`)
- Parsed date columns to datetime format
- Engineered `Length of Stay` from admission and discharge dates
- Clipped 108 negative billing values to 0 (0.19% of data)
- Dropped high cardinality columns unlikely to help modeling (`Name`, `Doctor`, `Hospital`, `Room Number`)
- Stripped whitespace from all string columns
- Verified zero null values

### 3. Feature Engineering (`src/features.py`)
- Binary encoded `Gender` (Male=0, Female=1)
- Label encoded `Test Results` (Normal=0, Inconclusive=1, Abnormal=2)
- One-hot encoded all remaining categorical columns (`Blood Type`, `Medical Condition`, `Insurance Provider`, `Admission Type`, `Medication`)
- MinMax scaled numeric columns (`Age`, `Billing Amount`, `Length of Stay`)
- Saved scaler to `models/scaler.pkl` for later inverse transformation
- Dropped date columns after feature extraction

### 4. Output
- Processed dataset saved to `data/processed/processed_dataset.csv`
- 55,500 rows × 27 feature columns, ready for modeling

---

## Exploratory Data Analysis

Key findings from `notebooks/eda.ipynb`:

- **Age** follows a near-uniform distribution (10–90), confirming synthetic generation
- **Billing Amount** is uniformly distributed (mean ~$25,539, kurtosis -1.19), not normally distributed
- **108 negative billing values** identified and handled via clipping
- **Zero outliers** detected via IQR method, consistent with uniform synthetic data
- Target variable `Test Results` is a 3-class classification problem

---

## How to Run

**1. Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Run the pipeline**
```bash
python main.py
```

First run builds the SQLite database and processes the data. Every subsequent run skips database creation and goes straight to loading.

**Expected output:**
```
=== Starting Healthcare Data Pipeline ===

✅ Database created from healthcare_dataset.csv
✅ Loaded data shape: (55500, 15)

--- Starting Data Cleaning ---
✅ Fixed name casing
✅ Parsed date columns
✅ Created Length of Stay column
✅ Clipped negative billing amounts
✅ Dropped high cardinality columns
✅ Stripped whitespace from string columns
✅ No null values found
--- Cleaning Complete: 55500 rows, 12 columns ---

--- Starting Feature Engineering ---
✅ Encoded Gender
✅ Encoded Test Results
✅ One-hot encoded categorical columns
✅ Scaled numeric columns
✅ Saved scaler to models/scaler.pkl
✅ Dropped date columns
--- Feature Engineering Complete: 55500 rows, 27 columns ---

✅ Saved processed data to: data/processed/processed_dataset.csv

=== Pipeline Complete ===
```

---

## Dependencies

```
pandas
numpy
scikit-learn
joblib
matplotlib
scipy
```

---

## Next Steps

- Build a classification model to predict `Test Results`
- Add SQL analytical queries (`sql/` folder)
- Connect processed data to Power BI for dashboard visualization
