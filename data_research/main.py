import os
import json
import pandas as pd
from sqlalchemy import create_engine

def run_research():
    db_url = "postgresql://admin:secretpassword@db:5432/analytics_db"
    report_dir = "/shared"
    report_path = os.path.join(report_dir, "research_report.json")

    print("Connecting to PostgreSQL...")
    engine = create_engine(db_url)

    print("Reading data...")
    df = pd.read_sql("SELECT * FROM raw_payments", engine)

    # Reapply your custom column names if the shape matches
    expected_cols = ['type', 'month', 'year', 'pkg_id', 'val1', 'pay_all', 'contract', 'date', 'name', 'doc', 'p_type', 'kekv', 'service']
    if len(df.columns) == len(expected_cols):
        df.columns = expected_cols

    print("Cleaning data...")
    df['pay_all'] = pd.to_numeric(df['pay_all'], errors='coerce')
    df = df.dropna(subset=['pay_all'])

    print("Calculating H1 (Concentration)...")
    top_10_threshold = df['pay_all'].quantile(0.9)
    top_10_sum = df[df['pay_all'] >= top_10_threshold]['pay_all'].sum()
    total_sum = df['pay_all'].sum()
    share = (top_10_sum / total_sum) * 100 if total_sum > 0 else 0

    print("Calculating H2 (Ownership Types)...")
    fop_avg = df[df['type'] == 'ФОП']['pay_all'].mean()
    knp_avg = df[df['type'] != 'ФОП']['pay_all'].mean()

    print("Calculating H3 (Time Activity)...")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_dates = df.dropna(subset=['date'])
    daily_activity = df_dates.groupby(df_dates['date'].dt.day)['pay_all'].count()

    peak_day = int(daily_activity.idxmax()) if not daily_activity.empty else 0
    peak_value = int(daily_activity.max()) if not daily_activity.empty else 0
    min_day = int(daily_activity.idxmin()) if not daily_activity.empty else 0
    min_value = int(daily_activity.min()) if not daily_activity.empty else 0
    ratio = peak_value / min_value if min_value > 0 else 0

    print("Generating JSON report...")
    report = {
        "h1_top_10_share_percentage": round(share, 2),
        "h2_fop_avg": round(fop_avg, 2) if pd.notna(fop_avg) else 0,
        "h2_knp_avg": round(knp_avg, 2) if pd.notna(knp_avg) else 0,
        "h3_peak_day": peak_day,
        "h3_peak_value": peak_value,
        "h3_min_day": min_day,
        "h3_min_value": min_value,
        "h3_activity_ratio": round(ratio, 1)
    }

    os.makedirs(report_dir, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)

    print(f"Research complete. Report saved to {report_path}")

if __name__ == "__main__":
    run_research()