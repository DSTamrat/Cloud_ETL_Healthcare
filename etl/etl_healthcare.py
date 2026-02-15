import os
import pandas as pd
from typing import Tuple

RAW_PATH = "data_raw/healthcare_admissions_raw.csv"
PROCESSED_PATH = "data_processed/healthcare_admissions_clean.csv"
AGG_PATH = "data_processed/healthcare_aggregated_metrics.csv"


def ingest_data(path: str = RAW_PATH) -> pd.DataFrame:
    print(f"Ingesting data from {path}...")
    df = pd.read_csv(path, parse_dates=['admission_date', 'discharge_date'])
    print(f"Loaded {len(df)} rows.")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print("Cleaning data...")

    before = len(df)
    df = df.drop_duplicates(subset=['patient_id', 'admission_date', 'hospital_unit'])
    after = len(df)
    print(f"Removed {before - after} duplicate rows.")

    df['primary_condition'] = df['primary_condition'].fillna('Unknown')

    median_cost = df['total_cost_usd'].median()
    df['total_cost_usd'] = df['total_cost_usd'].fillna(median_cost)

    df['length_of_stay_days'] = df['length_of_stay_days'].clip(lower=0.5)

    df['year'] = df['admission_date'].dt.year
    df['month'] = df['admission_date'].dt.month
    df['is_elderly'] = (df['age'] >= 65).astype(int)

    return df


def transform_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    print("Transforming data for analytics...")

    agg = (
        df.groupby(['hospital_unit', 'primary_condition'])
          .agg(
              admissions=('patient_id', 'count'),
              avg_los=('length_of_stay_days', 'mean'),
              readmission_rate=('readmitted_30d', 'mean'),
              avg_cost=('total_cost_usd', 'mean')
          )
          .reset_index()
    )

    agg['avg_los'] = agg['avg_los'].round(2)
    agg['readmission_rate'] = (agg['readmission_rate'] * 100).round(1)
    agg['avg_cost'] = agg['avg_cost'].round(2)

    return df, agg


def load_data(df_clean: pd.DataFrame, df_agg: pd.DataFrame,
              processed_path: str = PROCESSED_PATH,
              agg_path: str = AGG_PATH) -> None:
    print(f"Saving cleaned data to {processed_path}...")
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df_clean.to_csv(processed_path, index=False)

    print(f"Saving aggregated metrics to {agg_path}...")
    df_agg.to_csv(agg_path, index=False)

    print("Load step completed.")


def run_etl():
    df_raw = ingest_data()
    df_clean = clean_data(df_raw)
    df_clean, df_agg = transform_data(df_clean)
    load_data(df_clean, df_agg)


if __name__ == "__main__":
    run_etl()

