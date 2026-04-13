import os
import pandas as pd
from sqlalchemy import create_engine

def load_data():
    csv_path = "/app/data/raw/payments_2024.csv"
    db_url = "postgresql://admin:secretpassword@db:5432/analytics_db"

    if not os.path.exists(csv_path):
        print(f"Error: File not found at {csv_path}")
        return

    print("Reading CSV file...")
    df = pd.read_csv(csv_path, low_memory=False)

    print("Importing data to PostgreSQL...")
    engine = create_engine(db_url)
    df.to_sql('raw_payments', engine, if_exists='replace', index=False)

    print(f"Successfully imported {len(df)} rows.")

if __name__ == "__main__":
    load_data()