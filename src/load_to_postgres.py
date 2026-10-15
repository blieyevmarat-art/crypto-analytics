'''
Скрипт для загрузки CSV с котировками BTC в PostgreSQL
'''

import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

from src.analysis import BASE_DIR

BASE_DIR = Path(__file__).resolve().parent.parent

# Параметры подключения
DB_USER = 'analyst'
DB_PASSWORD = 'analyst123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'crypto_analytics'

# Строка подключения (connection string)
Connection_STRING = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def load_csv_to_postgres(csv_path:Path, table_name: str):
    '''
    Загружает CSV в указанную таблицу PostgreSQL.
    Если таблица существует - она будет заменена.
    '''

    # 1. Читаем CSV
    df = pd.read_csv(csv_path)
    df['open_time'] = pd.to_datetime(df['open_time'])
    print(f'Загружено строк из CSV: {len(df)}')

    # 2. Создаем подключение
    engine = create_engine(Connection_STRING)

    # 3. Записываем в PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f'Данные записаны в таблицу "{table_name}"')

if __name__=='__main__':
    csv_path = BASE_DIR / 'data' / 'raw' / 'btcusdt_1d.csv'
    load_csv_to_postgres(csv_path, table_name='btc_prices')