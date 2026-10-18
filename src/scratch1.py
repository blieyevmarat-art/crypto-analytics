import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from lxml.html.diff import group_by_first_item

# 1. Симулируем данные (как будто у нас 10.000 пользователей)
np.random.seed(42) # чтобы результаты были одинаковыми при каждом запуске
n_users = 10000

# Группа А (Красная кнопка): конверсия 10%
group_a = np.random.choice([0, 1], size=n_users, p=[0.90, 0.10])

# Группа Б (Зеленая кнопка): конверсия 11%
group_b = np.random.choice([0, 1], size=n_users, p=[0.89, 0.11])

# 2. Считаем базовые метрики
conv_a = group_a.mean()
conv_b = group_b.mean()

print(f'Конверсия в группе А (Красная): {conv_a:.2%}')
print(f'Конверсия в группе В (Зеленая): {conv_b:.2%}')
print(f'Разница: {(conv_b - conv_a):.2%}')

# 3. Проводим статистический тест (Т-тест)
# Он считает P-value - вероятность того что разница случайна
t_stat, p_value = stats.ttest_ind(group_a, group_b)

print(f'\nP_value: {p_value:.4f}')

# 4. Делаем вывод
if p_value < 0.05:
    print('Результат статистически значим, внедряем зеленую кнопку')
else:
    print('Результат не значим, разница может быть случайной, оставляем красную.')


# Визуализация
plt.figure(figsize=(6, 4))
plt.bar(['Группа А (Красная)', 'Группа В (Зеленая)'], [conv_a, conv_b], color=['#F7931A', '#2E86AB'])
plt.ylabel('Конверсия')
plt.title('Сравнение конверсии в А/В-тесте')
plt.ylim(0, 0.15)
plt.show()
