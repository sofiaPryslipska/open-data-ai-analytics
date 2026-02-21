import pandas as pd
import os


def check_data_quality():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_path, 'data', 'raw', 'payments_2024.csv')

    if not os.path.exists(file_path):
        print("Error: Data file not found.")
        return

    df = pd.read_csv(file_path)

    print("--- General Info ---")
    print(df.info())

    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    print("\n--- Duplicated Rows ---")
    print(f"Duplicates count: {df.duplicated().sum()}")

    print("\n--- Numerical Columns Summary ---")
    if 'pay_all' in df.columns:
        print(df['pay_all'].describe())
        negative_payments = (df['pay_all'] < 0).sum()
        print(f"Negative payments found: {negative_payments}")


if __name__ == "__main__":
    check_data_quality()