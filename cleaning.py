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

all_dfs = []

for year_folder in os.listdir('data/raw'):
    folder_path = f'data/raw/{year_folder}'

    if os.path.isdir(folder_path):
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.csv'):
                tour = file_name.replace(f'_{year_folder}.csv', '')
                df = pd.read_csv(f'data/raw/{year_folder}/{tour}_{year_folder}.csv')
                df['tour'] = tour
                df['year'] = year_folder
                all_dfs.append(df)

combined = pd.concat(all_dfs)
combined = combined.drop(columns=['Unnamed: 0', "Country"])
print(combined.shape)
print(combined.head())

print(combined.dtypes)
print(combined.isnull().sum())

combined['Prize $'] = combined['Prize $'].str.replace('$', '', regex=False)
combined['Prize $'] = combined['Prize $'].str.replace(',', '', regex=False)
combined['Prize $'] = combined['Prize $'].astype(float)

combined['Ride %'] = combined['Ride %'].str.replace('%', '', regex=False)
combined['Ride %'] = combined['Ride %'].astype(float)

combined['Points'] = pd.to_numeric(combined['Points'], errors='coerce')

combined['year'] = combined['year'].astype(int)

print(combined.dtypes)
print(combined.head())

combined.to_csv('data/cleaned/riders_2020-2026_clean.csv', index=False)
