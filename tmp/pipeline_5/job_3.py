
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

# Load preprocessed news data
df = pd.read_csv('preprocessed_news_data.txt')

# Tokenize the text data
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    
    # Lemmatize the tokens
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    # Join the tokens back into a string
    return ' '.join(tokens)

df['text'] = df['text'].apply(preprocess_text)

# Convert text data into numerical data using TF-IDF vectorization
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(df['text'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, df['sentiment'], test_size=0.2, random_state=42)

# Train a Naive Bayes classifier on the training data
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Test the classifier on the testing data
y_pred = classifier.predict(X_test)

# Evaluate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)

# Save the sentiment analysis results to a file
with open('sentiment_analysis_results.txt', 'w') as f:
    f.write('Sentiment Analysis Results:\n')
    f.write('Accuracy:', accuracy, '\n')</s>