import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

np.random.seed(42)

N_ROWS = 1000

def generate_healthcare_data(n_rows: int = N_ROWS) -> pd.DataFrame:
    patient_ids = np.arange(1, n_rows + 1)
    
    ages = np.random.randint(18, 90, size=n_rows)
    genders = np.random.choice(['Male', 'Female', 'Other'], size=n_rows, p=[0.48, 0.48, 0.04])
    conditions = np.random.choice(
        ['Hypertension', 'Diabetes', 'COPD', 'Heart Failure', 'Depression', 'None'],
        size=n_rows
    )
    admission_types = np.random.choice(
        ['Emergency', 'Elective', 'Urgent', 'Newborn'],
        size=n_rows
    )
    los_days = np.round(np.random.gamma(shape=2.0, scale=2.0, size=n_rows), 1)
    los_days = np.clip(los_days, 0.5, None)

    base_date = datetime(2023, 1, 1)
    admission_dates = [base_date + timedelta(days=int(x)) for x in np.random.randint(0, 365, size=n_rows)]
    discharge_dates = [d + timedelta(days=float(l)) for d, l in zip(admission_dates, los_days)]

    readmitted = np.random.choice([0, 1], size=n_rows, p=[0.8, 0.2])
    total_cost = np.round(los_days * np.random.uniform(800, 2500, size=n_rows), 2)

    hospital_units = np.random.choice(
        ['ICU', 'General Medicine', 'Surgery', 'Psychiatry', 'Cardiology'],
        size=n_rows
    )

    df = pd.DataFrame({
        'patient_id': patient_ids,
        'age': ages,
        'gender': genders,
        'primary_condition': conditions,
        'admission_type': admission_types,
        'length_of_stay_days': los_days,
        'admission_date': admission_dates,
        'discharge_date': discharge_dates,
        'readmitted_30d': readmitted,
        'total_cost_usd': total_cost,
        'hospital_unit': hospital_units
    })

    # introduce some missingness
    df.loc[np.random.rand(n_rows) < 0.05, 'total_cost_usd'] = np.nan
    df.loc[np.random.rand(n_rows) < 0.03, 'primary_condition'] = None

    return df


if __name__ == "__main__":
    os.makedirs("data_raw", exist_ok=True)
    df = generate_healthcare_data()
    df.to_csv("data_raw/healthcare_admissions_raw.csv", index=False)
    print("Generated data_raw/healthcare_admissions_raw.csv with", len(df), "rows")
