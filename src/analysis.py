'''
Модуль для анализа исторических данных о криптовалютах.
Считает метрики, добавляет скользящие средние, строит графики.
'''

import pandas as pd
import matplotlib
matplotlib.use('Agg') # Явно указываем бэкенд без окна
import matplotlib.pyplot as plt
from pathlib import Path

# Корень проекта - вычисляем один раз на уровне модуля
BASE_DIR = Path(__file__).resolve().parent.parent

def load_data(filepath: Path) -> pd.DataFrame:
    '''Загружает CSV и преобразует колонку с датой.'''
    df = pd.read_csv(filepath)
    df['open_time'] = pd.to_datetime(df['open_time'])
    return df

def calculate_metrics(df: pd.DataFrame) -> dict:
    '''
    Считает базовые метрики по цене закрытия

    Возвращает словарь с метриками:
    - средняя, медианная, минимальная, максимальная цена
    - стандартное отклонение
    - дневная волатильность (%)
    '''
    close = df['close']

    # Процентное изменение день ко дню (доходность)
    df['return'] = close.pct_change()

    metrics = {
        'mean_price': close.mean(),
        'median_price': close.median(),
        'min_price': close.min(),
        'max_price': close.max(),
        'std_price': close.std(),
        'volatility_daily_pct': df['return'].std() * 100,
        'total_return_pct': ((close.iloc[-1] / close.iloc[0]) - 1) * 100
    }
    return metrics

def add_moving_averages(df: pd.DataFrame, windows: list = [7,30]) -> pd.DataFrame:
    '''
    Добавляет колонки со скользящими средними.

    Параметры:
        df: DataFrame с колонкой close
        windows: список окон (7 - неделя, 30 - месяц)
    '''
    for w in windows:
        df[f'ma_{w}'] = df['close'].rolling(window=w).mean()
    return df

def plot_price_with_ma(df: pd.DataFrame, output_path: Path = None):
    '''Строит график цены закрытия с наложенными скользящими средними.'''
    fig, ax = plt.subplots(figsize=(14, 7))

    # Цена закрытия
    ax.plot(df['open_time'], df['close'], label='close', color='#F7931A', linewidth=1)

    # Скользящие средние
    for col in df.columns:
        if col.startswith('ma_'):
            ax.plot(df['open_time'], df[col], label=col.upper(), linewidth=1.5)

    ax.set_title('BTC/USDT - цена закрытия и скользящие средние', fontsize=14)
    ax.set_xlabel('Дата')
    ax.set_ylabel('Цена, USDT')
    ax.legend()
    ax.grid(True, alpha=0.3)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(output_path, dpi=100, bbox_inches='tight')
        print(f'График сохранен в {output_path}')

    plt.show()

if __name__ == '__main__':
    # 1. Загрузка
    data_path = BASE_DIR / 'data' / 'raw' / 'btcusdt_1d.csv'
    df = load_data(data_path)

    print(f'Загружено строк: {len(df)}')
    print(f'Период: {df["open_time"].min()} - {df["open_time"].max()}')

    # 2. Метрики
    metrics = calculate_metrics(df)
    print('\n=== Метрики ===')
    print(f'Средняя цена: {metrics["mean_price"]:.2f} USDT')
    print(f'Медианная цена: {metrics["median_price"]:.2f} USDT')
    print(f'Минимум: {metrics["min_price"]:.2f} USDT')
    print(f'Максимум: {metrics["max_price"]:.2f} USDT')
    print(f'Стандартное отклонение: {metrics["std_price"]:.2f}')
    print(f'Дневная волатильность: {metrics["volatility_daily_pct"]:.2f} %')
    print(f'Общая доходность: {metrics["total_return_pct"]:.2f} %')

    # 3. Скользящие средние
    df = add_moving_averages(df, windows=[7, 30])
    print(f'Колонка в df:', df.columns.tolist())
    print('ma_7 есть?', 'ma_7' in df.columns)
    print('ma_30 есть?', 'ma_30' in df.columns)

    # 4. График
    chart_path = BASE_DIR / 'data' / 'processed' / 'price_with_ma.png'
    plot_price_with_ma(df, output_path=chart_path)