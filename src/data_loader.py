'''
Модуль для загрузки данных.
Пока это заглушка, но скоро сдесь будет код для работы с Binance API.
'''
from http.client import responses

import requests
import pandas as pd

def check_connection():
	'''
	Проверяет соединение с Binance API.
	Возвращает текущую цену биткоина в USDT.
	'''
	
	url = "https://api.binance.com/api/v3/ticker/price"
	params = {"symbol": "BTCUSDT"}

	response = requests.get(url, params=params)
	data = response.json()

	price = float(data['price'])
	return price

def get_historical_klines(symbol: str, interval: str, limit: int = 1000):
    '''
    Загружает исторические свечи с Binance.

    Параметры:
        symbol (str): торговая пара, например 'BTCUSDT'
        interval (str): интервал свечи ('1d' - 1 день, '1h' - 1 час, '1m' - 1 минута)
        limit (int): сколько свечей загрузить (максимум 1000)

    Возвращает:
        pd.DataFrame: таблица с колонками open, high, close, volume
    '''
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': symbol,
        'interval': interval,
        'limit': limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Binance возвращает список списков. Превращаем DataFrame
    df = pd.DataFrame(data, columns=[
        'open_time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
    ])
    # Оставляем только нужные колонки
    df = df[['open_time', 'open', 'high', 'low', 'close', 'volume']]

    # Преаброзуем типы данных
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = df[col].astype(float)

    return df
if __name__ == '__main__':
      # Проверка связи
    try:
	    price = check_connection()
	    print(f'Текущая цена BTC/USDT: {price:.2f} USDT')
    except Exception as e:
        print(f'Ошибка при проверке связи: {e}')
        exit(1)
        # Загружаем 1000 дневных свечей
        print('\nЗагружаем 900 дневных свечей BTC/USDT...')
try:
    df = get_historical_klines('BTCUSDT', '1d', limit=900)
    print(f'\nЗагружено строк {len(df)}')
except Exception as e:
    print(f'Ошибка при запуске свечей: {e}')
    exit(1)
# Сохраняем в CSV
# Путь: data/raw/btcusdt_1d.csv
output_path = '../data/raw/btcusdt_1d.csv'
df.to_csv(output_path, index=False)
print(f'Данные сохранены в {output_path}')

print(f'Загружено строк: {len(df)}')
print(f'Период: с {df["open_time"].min()} по {df["open_time"].max}')
print('\nПервые 3 строки:')
print(df.head(3))