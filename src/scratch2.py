# 1. Считаем метрики для каждого дня
import pandas as pd
from IPython.core.display_functions import display
from fontTools.subset import subset

df['price_change_pct'] = df['close'].pct_change() * 100 # изменение цены в %
df['volatility'] = (df['high'] - df['low']) / df['open'] * 100 # волатильность (high-low)

# Очищаем от NAN (первый день будет NAN из-за pct_change)
df_rfm = df.dropna(subset=['price_change_pct']).copy()

# 2. Присваиваем баллы от 1 до 3 (где 3-максимум)
# Используем qcut, чтобы разбить на 3 равные группы (квантили)
df_rfm['R_score'] = pd.qcut(df_rfm['volatility'], 3, labels=[1, 2, 3]).astype(int)
df_rfm['F_score'] = pd.qcut(df_rfm['volume'], 3, labels=[1, 2, 3]).astype(int)
df_rfm['M_score'] = pd.qcut(df_rfm['price_change_pct'].abs(), 3, labels=[1, 2, 3]).astype(int)

# 3. Собираем RFM-сегмент (например, 333 - это максимальный риск)
df_rfm['RFM_segment'] = df_rfm['R_score'].astype(str) + df_rfm['F_score'].astype(str) + df_rfm['M_score'].astype(str)

# 4. Посмотрим на топ-5 самых волатильных дней (333)
print('=== Топ-5 самых волатильных дней (сегмент 333) ===')
top_volatile_days = df_rfm[df_rfm['RFM_segment'] == '333'][['open_time', 'close', 'price_change_pct', 'volatility']]
display(top_volatile_days.head(5))

# 5. Считаем, сколько дней в каждом сегменте (для понимания структуры рынка)
print('\n=== Распределение дней по сегментам ===')
segment_counts = df_rfm['RFM_segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Count']
display(segment_counts.head(10)) # топ-10 сегментов