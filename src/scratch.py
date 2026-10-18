# 1. Считаем скользящие средние на всем датафрейме
# (Не только на последних 100 днях, чтобы МА_30 посчиталась корректно)
from jedi.debug import increase_indent

df['MA_7'] = df['close'].rolling(window=7).mean()
df['MA_30'] = df['close'].rolling(window=30).mean()

# 2. Берем последние 100 дней для отрисовки
df_plot = df.tail(100)

# 3. Создаем график
fig = go.Figure()

# 3.1 Добавляем свечи
fig.add_trace(go.Candlestick(
    x=df_plot['open_time'],
    open=df_plot['open'],
    high=df_plot['high'],
    low=df_plot['low'],
    close=df_plot['close'],
    name='Цена (Свечи)',
    increasing_line_color='green',
    decreasing_line_color='red'
))

# 3.2 Добавляем МА_7 (синяя линия)
fig.add_trace(go.Scatter(
    x=df_plot['open_time'],
    y=df_plot['MA_7'],
    mode='lines',
    name='MA_7 (Неделя)',
    line=dict(color='#2E86AB', width=2)
))

# 3.3 Добавляем МА_30 (оранжевая линия)
fig.add_trace(go.Scatter(
    x=df_plot['open_time'],
    y=df_plot['MA_30'],
    mode='lines',
    name='MA_30 (Месяц)',
    line=dict(color='#F7931A', width=2)
))

# 4. Настраиваем внешний вид
fig.update_layout(
    title='BTC/USDT - Свечи с МА_7 и МА_30',
    yaxis_title='Цена (USDT)',
    xaxis_title='Дата',
    template='plotly_dark',
    # Убираем ползунок (range slider) внизу, чтобы было чище
    xaxis_rangeslider_visible=False
)

fig.show()