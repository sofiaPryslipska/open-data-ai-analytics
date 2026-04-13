import os
import pandas as pd
from sqlalchemy import create_engine


def check_data_quality():
    db_url = "postgresql://admin:secretpassword@db:5432/analytics_db"
    report_dir = "/shared"
    report_path = os.path.join(report_dir, "quality_report.txt")

    print("Connecting to PostgreSQL...")
    engine = create_engine(db_url)

    print("Reading data...")
    df = pd.read_sql("SELECT * FROM raw_payments", engine)

    print("Analyzing quality metrics...")

    report_content = [
        "Data Quality Report",
        "===================",
        f"Total records: {len(df)}",
        f"Duplicated rows: {df.duplicated().sum()}",
        "\n--- Missing Values ---",
        df.isnull().sum().to_string(),
        "\n--- Data Types ---",
        df.dtypes.to_string()
    ]

    if 'pay_all' in df.columns:
        df['pay_all'] = pd.to_numeric(df['pay_all'], errors='coerce')
        report_content.extend([
            "\n--- 'pay_all' Column Analysis ---",
            df['pay_all'].describe().to_string(),
            f"Negative payments count: {(df['pay_all'] < 0).sum()}"
        ])

    os.makedirs(report_dir, exist_ok=True)

    with open(report_path, 'w') as f:
        f.write('\n'.join(report_content))

    print(f"Analysis complete. Report saved to {report_path}")


if __name__ == "__main__":
    check_data_quality()