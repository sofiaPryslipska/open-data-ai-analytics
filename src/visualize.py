import pandas as pd
import matplotlib.pyplot as plt
import os

def create_visualizations():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, 'data', 'raw', 'payments_2024.csv')
    save_dir = os.path.join(base_path, 'reports', 'figures')
    os.makedirs(save_dir, exist_ok=True)

    cols = ['type', 'm', 'y', 'pkg', 'v1', 'pay', 'num', 'date', 'name', 'doc', 't', 'k', 's']
    df = pd.read_csv(file_path, names=cols, skiprows=1, low_memory=False)
    df['pay'] = pd.to_numeric(df['pay'], errors='coerce')
    df = df.dropna(subset=['pay'])

    # H1: Pie chart
    top_10_threshold = df['pay'].quantile(0.9)
    shares = [df[df['pay'] >= top_10_threshold]['pay'].sum(), df[df['pay'] < top_10_threshold]['pay'].sum()]
    plt.figure(figsize=(8, 6))
    plt.pie(shares, labels=['Top 10%', 'Others'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff'])
    plt.title('Budget Concentration (H1)')
    plt.savefig(os.path.join(save_dir, 'h1_concentration.png'))

    # H3: Bar chart (активність по днях)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    plt.figure(figsize=(12, 6))
    df.groupby(df['date'].dt.day)['pay'].count().plot(kind='bar', color='skyblue')
    plt.title('Transaction Activity by Day (H3)')
    plt.xlabel('Day of Month')
    plt.ylabel('Count')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(os.path.join(save_dir, 'h3_daily_activity.png'))

if __name__ == "__main__":
    create_visualizations()