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
