"""
Скрипт для загрузки исторических данных о Bitcoin через Yahoo Finance.
Используется как альтернатива Binance API (который может быть заблокирован).
"""

import yfinance as yf
import pandas as pd
from pathlib import Path

def download_btc_data(period: str = "2y", interval: str = "1d") -> pd.DataFrame:
    """
    Скачивает исторические данные по BTC-USD через Yahoo Finance.

    Параметры:
    period (str): период ('2y' — 2 года, '1y' — 1 год, '6mo' — 6 месяцев)
    interval (str): интервал свечи ('1d' — 1 день, '1h' — 1 час)

    Возвращает:
    pd.DataFrame: таблица с колонками open, high, low, close, volume
    """
    print(f"Скачиваем данные BTC-USD за период: {period}...")

    # Скачиваем данные через yfinance
    ticker = yf.Ticker("BTC-USD")
    df = ticker.history(period=period, interval=interval)

    # Сбрасываем индекс (дата становится колонкой)
    df = df.reset_index()

    # Переименовываем колонки в тот же формат, что был у Binance
    df = df.rename(columns={
        "Date": "open_time",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    # Оставляем только нужные колонки
    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    # Приводим типы данных
    df["open_time"] = pd.to_datetime(df["open_time"]).dt.tz_localize(None)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)

    return df


if __name__ == "__main__":
    # Вычисляем корень проекта (на 2 уровня выше: src/download_data.py -> src/ -> crypto_analytics)
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Создаем папки
    (BASE_DIR / 'data' / 'raw').mkdir(parents=True, exist_ok=True)
    (BASE_DIR / 'data' / 'processed').mkdir(parents=True, exist_ok=True)

    df = download_btc_data(period="2y", interval="1d")

    output_path = BASE_DIR / 'data' / 'raw' / 'btcusdt_1d.csv'
    df.to_csv(output_path, index=False)

    print(f"✅ Данные сохранены в {output_path}")
    print(f"Загружено строк: {len(df)}")
    print(f"Период: с {df['open_time'].min()} по {df['open_time'].max()}")
    print("\nПервые 3 строки:")
    print(df.head(3))
