"""產生模擬電商資料集"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# 設定參數
n_orders = 5000
start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# 產生訂單日期
days_range = (end_date - start_date).days
order_dates = [start_date + timedelta(days=np.random.randint(0, days_range)) for _ in range(n_orders)]

# 產品類別與價格範圍
categories = {
    'Electronics': (50, 2000),
    'Clothing': (10, 200),
    'Home & Kitchen': (15, 500),
    'Books': (5, 50),
    'Sports': (20, 300),
    'Beauty': (5, 150),
    'Toys': (10, 100),
}

# 美國州份
states = ['California', 'Texas', 'New York', 'Florida', 'Illinois',
          'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan',
          'New Jersey', 'Virginia', 'Washington', 'Arizona', 'Massachusetts']

# 產生資料
data = []
for i in range(n_orders):
    cat = np.random.choice(list(categories.keys()),
                           p=[0.25, 0.20, 0.15, 0.12, 0.10, 0.10, 0.08])
    price_min, price_max = categories[cat]
    quantity = np.random.randint(1, 5)
    unit_price = round(np.random.uniform(price_min, price_max), 2)
    satisfaction = min(5, max(1, round(np.random.normal(3.8, 0.8))))
    delivery_days = max(1, int(np.random.normal(5, 2)))

    data.append({
        'order_id': f'ORD-{i+1:05d}',
        'order_date': order_dates[i].strftime('%Y-%m-%d'),
        'category': cat,
        'product_name': f'{cat}_Product_{np.random.randint(1, 50)}',
        'quantity': quantity,
        'unit_price': unit_price,
        'total_amount': round(unit_price * quantity, 2),
        'state': np.random.choice(states),
        'customer_satisfaction': satisfaction,
        'delivery_days': delivery_days,
    })

df = pd.DataFrame(data)
df.to_csv('ecommerce_data/orders.csv', index=False)
print(f"已產生 {len(df)} 筆訂單資料 → ecommerce_data/orders.csv")
print(f"日期範圍: {df['order_date'].min()} ~ {df['order_date'].max()}")
print(f"類別: {df['category'].nunique()} 種")
print(f"總營收: ${df['total_amount'].sum():,.2f}")
