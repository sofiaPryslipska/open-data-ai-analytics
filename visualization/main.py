import os
import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


def create_visualizations():
    db_url = "postgresql://admin:secretpassword@db:5432/analytics_db"
    save_dir = "/shared/plots"

    print("Connecting to PostgreSQL...")
    engine = create_engine(db_url)

    print("Reading data...")
    df = pd.read_sql("SELECT * FROM raw_payments", engine)

    expected_cols = ['type', 'month', 'year', 'pkg_id', 'val1', 'pay_all', 'contract', 'date', 'name', 'doc', 'p_type',
                     'kekv', 'service']
    if len(df.columns) == len(expected_cols):
        df.columns = expected_cols

    print("Cleaning data...")
    df['pay_all'] = pd.to_numeric(df['pay_all'], errors='coerce')
    df = df.dropna(subset=['pay_all'])

    os.makedirs(save_dir, exist_ok=True)

    print("Generating H1 chart...")
    top_10_threshold = df['pay_all'].quantile(0.9)
    shares = [df[df['pay_all'] >= top_10_threshold]['pay_all'].sum(),
              df[df['pay_all'] < top_10_threshold]['pay_all'].sum()]

    plt.figure(figsize=(8, 6))
    plt.pie(shares, labels=['Top 10%', 'Others'], autopct='%1.1f%%', colors=['#ff9999', '#66b3ff'])
    plt.title('Budget Concentration (H1)')
    plt.savefig(os.path.join(save_dir, 'h1_concentration.png'))
    plt.close()

    print("Generating H3 chart...")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df_dates = df.dropna(subset=['date'])

    plt.figure(figsize=(12, 6))
    df_dates.groupby(df_dates['date'].dt.day)['pay_all'].count().plot(kind='bar', color='skyblue')
    plt.title('Transaction Activity by Day (H3)')
    plt.xlabel('Day of Month')
    plt.ylabel('Count')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(os.path.join(save_dir, 'h3_daily_activity.png'))
    plt.close()

    print(f"Visualizations saved to {save_dir}")


if __name__ == "__main__":
    create_visualizations()