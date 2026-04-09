import requests
import os


def download_data():
    url = "https://data.gov.ua/dataset/9ebd7456-2992-450f-bd9f-fdaf083bab20/resource/86668bef-3c1b-447a-a072-51894c6ad0b9/download/payments_on_contracts_pmg_2024.csv"

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base_path, 'data', 'raw', 'payments_2024.csv')

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)


if __name__ == "__main__":
    download_data()