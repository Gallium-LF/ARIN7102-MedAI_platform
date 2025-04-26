# 读取数据
tafeng = pd.read_csv('ta_feng.csv')

# 1. 清洗数据
tafeng = tafeng[tafeng['QUANTITY'] > 0]  # 删除数量<=0的
tafeng = tafeng[tafeng['SALES_AMOUNT'] > 0]  # 删除金额<=0的
tafeng = tafeng.dropna()  # 删除空值

# 2. 时间处理
tafeng['TRANSACTION_DT'] = pd.to_datetime(tafeng['TRANSACTION_DT'])
tafeng['Year'] = tafeng['TRANSACTION_DT'].dt.year
tafeng['Month'] = tafeng['TRANSACTION_DT'].dt.month
tafeng['Day'] = tafeng['TRANSACTION_DT'].dt.day
tafeng['Weekday'] = tafeng['TRANSACTION_DT'].dt.weekday
tafeng['Hour'] = tafeng['TRANSACTION_DT'].dt.hour

# 3. 促销标记处理
tafeng['PROMOTION_FLG'] = tafeng['PROMOTION_FLG'].fillna('NoPromo')

# 4. 生成RFM特征
snapshot_date = tafeng['TRANSACTION_DT'].max() + pd.Timedelta(days=1)
rfm_tafeng = tafeng.groupby('CUSTOMER_ID').agg({
    'TRANSACTION_DT': lambda x: (snapshot_date - x.max()).days,
    'TRANSACTION_ID': 'nunique',
    'SALES_AMOUNT': 'sum'
})
rfm_tafeng.rename(columns={
    'TRANSACTION_DT': 'Recency',
    'TRANSACTION_ID': 'Frequency',
    'SALES_AMOUNT': 'Monetary'
}, inplace=True)

# 5. 保存处理结果
tafeng.to_csv('tafeng_cleaned.csv', index=False)
rfm_tafeng.to_csv('tafeng_rfm.csv')
print('Ta-Feng data cleaned and RFM table saved.')
