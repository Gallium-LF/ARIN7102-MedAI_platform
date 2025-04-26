import pandas as pd

# 1. 读取数据
orders = pd.read_csv('orders.csv')
order_products_prior = pd.read_csv('order_products__prior.csv')
products = pd.read_csv('products.csv')
aisles = pd.read_csv('aisles.csv')
departments = pd.read_csv('departments.csv')

# 2. 合并表格
order_products = order_products_prior.merge(products, on='product_id', how='left')
order_products = order_products.merge(aisles, on='aisle_id', how='left')
order_products = order_products.merge(departments, on='department_id', how='left')

# 3. 合并订单表
full_data = order_products.merge(orders, on='order_id', how='left')

# 4. 清洗数据
full_data.dropna(inplace=True)  # 删除含有缺失值的行

# 5. 处理时间特征
full_data['order_hour_of_day_bins'] = pd.cut(
    full_data['order_hour_of_day'],
    bins=[-1,5,11,17,21,24],
    labels=['Late Night','Morning','Afternoon','Evening','Late Night2']
)

# 6. 输出清洗后数据
full_data.to_csv('instacart_cleaned.csv', index=False)
print('Instacart data cleaned and saved.')
