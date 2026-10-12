'''
Модуль для загрузки данных.
Пока это заглушка, но скоро сдесь будет код для работы с Binance API.
'''

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


if __name__ == '__main__':
	price = check_connection()
	print(f'Текущая цена BTC/USDT: {price:.2f} USDT')
