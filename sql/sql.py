import pandas as pd
from sqlalchemy import create_engine

#Підключення до PostgreSQL
engine = create_engine('postgresql://postgres:avataranaconda2011@localhost:5432/pbr_analytics')

#Завантаження зібраного та очищеного CSV
df = pd.read_csv('../data/cleaned/riders_2020-2026_clean.csv')

#Завантаження файлу в PostgreSQL як таблиці
df.columns = df.columns.str.lower().str.replace(' ', '_')
df.to_sql('riders', engine, if_exists='replace', index=False)


print('Done. Rows uploaded: ', len(df))