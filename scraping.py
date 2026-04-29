import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
tours = {
    "unleash_the_best": "PBR-US",
    "pendleton_whisky_velocity_tour": ["VELO-G", 'VELO'],
    "touring_pro_division": "TPD-US",
    "pbr_australia": "PBR-AU",
    "pbr_canada": "PBR-CA",
    "pbr_brazil": "PBR-BR",
    "challenger_series": "CHLG-G"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

for year in years:
    for tour_name, tour_code in tours.items():
        # перетворення в список
        if isinstance(tour_code, str):
            tour_code = [tour_code]

        # кожен код проходить посилання
        table = None
        for code in tour_code:
            url = f'https://www.pbr.com/athletes/riders/standings/{year}/{code}'
            response = requests.get(url, headers=headers)
            print(f"Status: {response.status_code}")
            print(f"Has table: {'<table' in response.text}")

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            if table is not None:
                print(f"Table found for {year}/{tour_name} with code {code}")
                break

        # якщо таблиці нема, пропускаємо
        if table is None:
            print(f"No table for {year}/{tour_name} — skipping")
            continue

        # витягуєм заголовки
        headers_row = []
        for th in table.find_all('th'):
            headers_row.append(th.get_text(strip=True))

        # витягуєм рядки
        all_rows = []
        for row in table.find_all('tr'):
            cell_each_row = []
            for td in row.find_all('td'):
                cell_each_row.append(td.get_text(strip=True))
            all_rows.append(cell_each_row)

        # фільтруємо порожні рядки
        filtered_rows = []
        for row in all_rows:
            if len(row) > 0:
                filtered_rows.append(row)

        if len(filtered_rows) == 0:
            continue

        # датафрейм і збереження
        tour_name_DF = pd.DataFrame(filtered_rows, columns=headers_row)
        tour_name_DF = tour_name_DF[tour_name_DF['Rider'].notna()]

        os.makedirs(f'data/raw/{year}', exist_ok=True)
        tour_name_DF.to_csv(f'data/raw/{year}/{tour_name}_{year}.csv')
        print(f"Saved: {year}/{tour_name} — {len(tour_name_DF)} riders")
        print('-------------------------------------------------')
