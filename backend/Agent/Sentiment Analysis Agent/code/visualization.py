import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import joblib

train_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_train.csv")
test_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_test.csv")
train_df2 = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_train2.csv")
test_df2 = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_test2.csv")
# wordcloud
sentiments = ['negative', 'neutral', 'positive']
plt.figure(figsize=(15, 5))
for i, sentiment in enumerate(sentiments):
    text = ' '.join(train_df[train_df['sentiment'] == sentiment]['review'])
    wordcloud = WordCloud(width=600, height=400, background_color='white').generate(text)
    plt.subplot(1, 3, i + 1)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"{sentiment.capitalize()} Sentiment")
plt.show()

sentiments2 = ['negative', 'positive']
plt.figure(figsize=(15, 5))
for i, sentiment in enumerate(sentiments2):
    text = ' '.join(train_df[train_df['sentiment'] == sentiment]['review'])
    wordcloud = WordCloud(width=600, height=400, background_color='white').generate(text)
    plt.subplot(1, 2, i + 1)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"{sentiment.capitalize()} Sentiment")
plt.show()

features = ['condition', 'usefulCount', 'day', 'month', 'Year',
            'count_word', 'count_unique_word', 'count_letters',
            'count_punctuations', 'count_words_upper', 'count_words_title',
            'count_stopwords', 'mean_word_len']

corr_matrix = train_df[features].corr()

# heat map
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()
