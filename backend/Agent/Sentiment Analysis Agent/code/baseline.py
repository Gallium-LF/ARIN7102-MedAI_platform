import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

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
tfidf = TfidfVectorizer(max_features=5000)
X_train = tfidf.fit_transform(train_df['review'].astype(str))
X_test = tfidf.transform(test_df['review'].astype(str))

logreg = LogisticRegression(max_iter=1000)
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.4f}")
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))