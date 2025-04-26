import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from lightgbm import LGBMClassifier, plot_importance
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
import seaborn as sns
import joblib

train_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_train.csv")
test_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_test.csv")
sentiment_mapping = {'negative': 0, 'positive': 1}
def map_sentiment(rating):
    if rating <= 5:
        return 'negative'
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

train_df.to_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_train2.csv", index=False)
test_df.to_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_test2.csv", index=False)

features = ['condition', 'usefulCount', 'day', 'month', 'Year',
            'count_word', 'count_unique_word', 'count_letters',
            'count_punctuations', 'count_words_upper', 'count_words_title',
            'count_stopwords', 'mean_word_len']
X_train_structured = train_df[features]
X_test_structured = test_df[features]

tfidf = TfidfVectorizer(max_features=5000)
X_train_tfidf = tfidf.fit_transform(train_df['review'].astype(str))
X_test_tfidf = tfidf.transform(test_df['review'].astype(str))
X_train = hstack([X_train_structured, X_train_tfidf])
X_test = hstack([X_test_structured, X_test_tfidf])

sentiment_mapping = {'negative': 0, 'positive': 1}
y_train = train_df['sentiment'].map(sentiment_mapping)
y_test = test_df['sentiment'].map(sentiment_mapping)

lgbm = LGBMClassifier(
    n_estimators=10000,
    learning_rate=0.10,
    num_leaves=30,
    subsample=.9,
    max_depth=7,
    reg_alpha=.1,
    reg_lambda=.1,
    min_split_gain=.01,
    min_child_weight=2,
    silent=-1,
    verbose=-1,
)
model = lgbm.fit(X_train, y_train)

y_pred = lgbm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:\n", class_report)
print("Confusion Matrix:\n", conf_matrix)

joblib.dump(lgbm, "/Users/wujoy/Desktop/7102project/lgbm_model2.pkl")
