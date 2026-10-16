-- Базовые метрики
SELECT
	COUNT(*) AS total_rows,
	MIN(close) AS min_price,
	MAX(close) AS max_price,
	AVG(close) AS avg_price,
	STDDEV(close) AS std_price
FROM btc_prices;

-- Средняя цена по месяцам
SELECT
	DATE_TRUNC('month', open_time) AS month,
	AVG(close) AS avg_price,
	COUNT(*) AS days
FROM btc_prices
GROUP BY month
ORDER BY month;

-- Топ 5 самых волотильных месяцев
SELECT
	DATE_TRUNC('month', open_time) AS month,
	MAX(close) - MIN(close) AS price_range,
	ROUND(CAST((MAX(close) - MIN(close)) / AVG(close) * 100 AS numeric), 2) AS range_pct
FROM btc_prices
GROUP BY month
ORDER BY range_pct DESC
LIMIT 5;


-- Запрос с LAG
SELECT
	open_time,
	close,
	LAG(close) OVER (ORDER BY open_time) AS prev_close,
	ROUND(
		CAST(
			(close - LAG(close) OVER (ORDER BY open_time))
			/ LAG(close) OVER (ORDER BY open_time) * 100
			AS numeric
		),
		2
	) AS daily_return_pct
FROM btc_prices
ORDER BY open_time
LIMIT 10;

-- Оконная функция, посчитать волотильность
WITH daily_returns AS (
	SELECT
		open_time,
		(close - LAG(close) OVER (ORDER BY open_time))
		/ LAG(close) OVER (ORDER BY open_time) * 100 AS return_pct
	FROM btc_prices
)
SELECT
	ROUND(CAST(STDDEV(return_pct) AS numeric), 2) AS daily_volatility_pct
FROM daily_returns
WHERE return_pct IS NOT NULL;