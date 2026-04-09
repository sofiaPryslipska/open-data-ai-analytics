import pandas as pd
import os


def run_research():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, 'data', 'raw', 'payments_2024.csv')

    if not os.path.exists(file_path):
        print("Error: File not found.")
        return

    cols = ['type', 'month', 'year', 'pkg_id', 'val1', 'pay_all', 'contract', 'date', 'name', 'doc', 'p_type', 'kekv',
            'service']
    df = pd.read_csv(file_path, names=cols, skiprows=1, low_memory=False)

    df['pay_all'] = pd.to_numeric(df['pay_all'], errors='coerce')
    df = df.dropna(subset=['pay_all'])

    # H1: Нерівномірність виплат
    top_10_threshold = df['pay_all'].quantile(0.9)
    top_10_sum = df[df['pay_all'] >= top_10_threshold]['pay_all'].sum()
    total_sum = df['pay_all'].sum()
    share = (top_10_sum / total_sum) * 100
    print(f"H1: Top 10% of payments concentrate {share:.2f}% of total budget")

    # H2: Типи власності
    fop_avg = df[df['type'] == 'ФОП']['pay_all'].mean()
    knp_avg = df[df['type'] != 'ФОП']['pay_all'].mean()
    print(f"H2: Avg payment: FOP = {fop_avg:.2f}, KNP = {knp_avg:.2f}")

    # H3: Часова активність
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    daily_activity = df.groupby(df['date'].dt.day)['pay_all'].count()

    peak_day = daily_activity.idxmax()
    peak_value = daily_activity.max()
    min_day = daily_activity.idxmin()
    min_value = daily_activity.min()

    print(f"H3: Activity range: Min = {min_value} (day {min_day}), Max = {peak_value} (day {peak_day})")
    print(f"Conclusion: Activity at peak is {peak_value / min_value:.1f}x higher than at minimum.")


if __name__ == "__main__":
    run_research()