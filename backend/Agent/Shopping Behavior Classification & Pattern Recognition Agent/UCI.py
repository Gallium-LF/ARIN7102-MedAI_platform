# 读取数据
retail = pd.read_excel('Online Retail.xlsx')

# 1. 清洗缺失值和异常值
retail = retail.dropna(subset=['CustomerID'])  # 删除CustomerID为空的行
retail = retail[retail['Quantity'] > 0]  # 删除数量负数
retail = retail[retail['UnitPrice'] > 0]  # 删除价格为负的记录

# 2. 去除退货单
retail = retail[~retail['InvoiceNo'].astype(str).str.startswith('C')]

# 3. 添加时间特征
retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'])
retail['Year'] = retail['InvoiceDate'].dt.year
retail['Month'] = retail['InvoiceDate'].dt.month
retail['Day'] = retail['InvoiceDate'].dt.day
retail['Weekday'] = retail['InvoiceDate'].dt.weekday
retail['Hour'] = retail['InvoiceDate'].dt.hour

# 4. 计算RFM特征
snapshot_date = retail['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = retail.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
    'InvoiceNo': 'count',
    'TotalPrice': lambda x: (x.Quantity * x.UnitPrice).sum()
})
rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalPrice': 'Monetary'
}, inplace=True)

# 5. 保存处理结果
retail.to_csv('online_retail_cleaned.csv', index=False)
rfm.to_csv('online_retail_rfm.csv')
print('Online Retail data cleaned and RFM table saved.')
