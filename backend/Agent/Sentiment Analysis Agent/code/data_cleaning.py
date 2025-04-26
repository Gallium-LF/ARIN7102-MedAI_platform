import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer

train_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/drugsComTrain_raw.csv")
test_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/drugsComTest_raw.csv")

train_df = train_df.dropna(subset=['condition'])
test_df = test_df.dropna(subset=['condition'])

sentiment_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
def map_sentiment(rating):
    if rating <= 3:
        return 'negative'
    elif 4 <= rating <= 6:
        return 'neutral'
    else:
        return 'positive'

train_df['sentiment'] = train_df['rating'].apply(map_sentiment)
test_df['sentiment'] = test_df['rating'].apply(map_sentiment)

y_train = train_df['sentiment'].map(sentiment_mapping)
y_test = test_df['sentiment'].map(sentiment_mapping)

le = LabelEncoder()
train_df['condition'] = le.fit_transform(train_df['condition'])
test_df['condition'] = test_df['condition'].map(lambda x: le.transform([x])[0] if x in le.classes_ else -1)

def extract_text_features(df):
    df['count_word'] = df['review'].apply(lambda x: len(str(x).split()))
    df['count_unique_word'] = df['review'].apply(lambda x: len(set(str(x).split())))
    df['count_letters'] = df['review'].apply(lambda x: len(str(x)))
    df['count_punctuations'] = df['review'].apply(lambda x: sum([1 for c in str(x) if c in '!?.,;:']))
    df['count_words_upper'] = df['review'].apply(lambda x: sum([1 for w in str(x).split() if w.isupper()]))
    df['count_words_title'] = df['review'].apply(lambda x: sum([1 for w in str(x).split() if w.istitle()]))
    df['count_stopwords'] = df['review'].apply(lambda x: sum([1 for w in str(x).lower().split() if w in {'the', 'and', 'is', 'in', 'it', 'of', 'to', 'this'}]))
    df['mean_word_len'] = df['review'].apply(lambda x: np.mean([len(w) for w in str(x).split()]))
    return df

train_df = extract_text_features(train_df)
test_df = extract_text_features(test_df)

train_df['date'] = pd.to_datetime(train_df['date'])
test_df['date'] = pd.to_datetime(test_df['date'])
train_df['day'] = train_df['date'].dt.day
test_df['day'] = test_df['date'].dt.day
train_df['month'] = train_df['date'].dt.month
test_df['month'] = test_df['date'].dt.month
train_df['Year'] = train_df['date'].dt.year
test_df['Year'] = test_df['date'].dt.year

train_df.to_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_train.csv", index=False)
test_df.to_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_test.csv", index=False)

print("Data cleaning completed and saved.")
