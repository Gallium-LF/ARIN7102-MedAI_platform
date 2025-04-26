# 1. Import Libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import roc_auc_score, precision_score, recall_score
from mlxtend.frequent_patterns import fpgrowth, association_rules
from prefixspan import PrefixSpan
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# 2. Load Cleaned Data
instacart = pd.read_csv('instacart_cleaned.csv')
online_retail = pd.read_csv('online_retail_cleaned.csv')
tafeng = pd.read_csv('tafeng_cleaned.csv')

# 3. Feature Engineering Function
def build_features(df, id_col, recency_col, freq_col, monetary_col, promo_col, time_bin_col):
    feat = df.groupby(id_col).agg({
        recency_col: 'max',
        freq_col: 'count',
        monetary_col: 'sum',
        promo_col: 'mean'
    }).rename(columns={
        recency_col: 'Recency',
        freq_col: 'Frequency',
        monetary_col: 'Monetary',
        promo_col: 'PromoSensitivity'
    })
    # One-hot encode time bins
    times = pd.get_dummies(df[[id_col, time_bin_col]].set_index(id_col), prefix='Time')
    feat = feat.join(times.groupby(level=0).mean())
    return feat.reset_index()

# 4. Build Feature Tables
insta_feat  = build_features(instacart,  'user_id',      'order_number', 'order_id',    'reordered',  'reordered',  'order_hour_of_day_bins')
retail_feat = build_features(online_retail,'CustomerID',   'InvoiceDate',  'InvoiceNo',   'TotalPrice', 'PromoFlag',  'HourBin')
tafeng_feat = build_features(tafeng,      'CUSTOMER_ID',  'TRANSACTION_DT','TRANSACTION_ID','SALES_AMOUNT','PROMOTION_FLG','TimeBin')

# 5. Merge Feature Tables on User ID
data = insta_feat.merge(retail_feat, how='inner', left_on='user_id', right_on='CustomerID')
data = data.merge(tafeng_feat, how='inner', left_on='user_id', right_on='CUSTOMER_ID')

# 6. Prepare for Clustering
features = [c for c in data.columns if c not in ['user_id','CustomerID','CUSTOMER_ID']]
X = StandardScaler().fit_transform(data[features])

# 7. Clustering: K-Means + DBSCAN Noise Detection
kmeans = KMeans(n_clusters=4, random_state=42).fit(X)
data['cluster'] = kmeans.labels_
dbscan = DBSCAN(eps=1.5, min_samples=5).fit(X)
data['noise'] = (dbscan.labels_ == -1)

# 8. VIP Prediction: Random Forest with GridSearchCV
data['is_VIP'] = ((data['Frequency'] >= 10) & (data['Monetary'] >= 500)).astype(int)
Xv, yv = data[features], data['is_VIP']
X_train, X_test, y_train, y_test = train_test_split(Xv, yv, test_size=0.2, random_state=42)

param_grid = {'n_estimators':[100,200], 'max_depth':[5,10,None]}
rf_cv = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, scoring='roc_auc')
rf_cv.fit(X_train, y_train)

y_proba = rf_cv.predict_proba(X_test)[:,1]
y_pred  = rf_cv.predict(X_test)
print('AUC:',   roc_auc_score(y_test, y_proba))
print('Prec@10%:', precision_score(y_test, y_pred))
print('Recall@10%:', recall_score(y_test, y_pred))

# 9. Association Rule Mining (FP-Growth)
basket = instacart.pivot_table(
    index='order_id', columns='product_id', values='add_to_cart_order',
    aggfunc=lambda x: 1, fill_value=0
)
freq_itemsets = fpgrowth(basket, min_support=0.005, use_colnames=True)
rules = association_rules(freq_itemsets, metric='lift', min_threshold=1)
print(rules.sort_values('lift', ascending=False).head(10))

# 10. Sequential Pattern Mining (PrefixSpan)
sequences = instacart.groupby('user_id')['product_id'].apply(list).tolist()
ps = PrefixSpan(sequences)
patterns = ps.frequent(0.01)
print('Top Sequential Patterns:', patterns[:10])

# 11. Path Modeling: Sankey Diagram
states = ['Promo Page','Product Page','Add to Cart','Checkout']
source = [0,1,2]; target = [1,2,3]; value = [1000,600,400]
fig = go.Figure(data=[go.Sankey(
    node=dict(label=states, pad=15, thickness=20),
    link=dict(source=source, target=target, value=value)
)])
fig.update_layout(title_text="User Shopping Path Sankey", font_size=12)
fig.show()

# 12. Visualization: PCA Scatter & Feature Importance
pca_res = PCA(n_components=2).fit_transform(X)
plt.figure(figsize=(8,6))
sns.scatterplot(x=pca_res[:,0], y=pca_res[:,1], hue=data['cluster'], palette='Set2')
plt.title('Clusters (PCA View)')
plt.show()

feat_imp = pd.Series(rf_cv.best_estimator_.feature_importances_, index=features).sort_values()
plt.figure(figsize=(8,6))
feat_imp.plot(kind='barh')
plt.title('Feature Importance for VIP Prediction')
plt.show()
