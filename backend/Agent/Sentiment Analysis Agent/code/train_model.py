import pandas as pd
import numpy as np
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

train_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_train.csv")
test_df = pd.read_csv("/Users/wujoy/Desktop/7102project/archive/cleaned_test.csv")

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

sentiment_mapping = {'negative': 0, 'neutral': 1, 'positive': 2}
y_train = train_df['sentiment'].map(sentiment_mapping)
y_test = test_df['sentiment'].map(sentiment_mapping)

class_weights = {0: 1, 1: 5, 2: 1} 
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
    class_weight=class_weights,
)
lgbm.fit(X_train, y_train)

y_pred = lgbm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
class_report = classification_report(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:\n", class_report)
print("Confusion Matrix:\n", conf_matrix)

joblib.dump(lgbm, "/Users/wujoy/Desktop/7102project/lgbm_model.pkl")
joblib.dump(tfidf, "/Users/wujoy/Desktop/7102project/tfidf_vectorizer.pkl")