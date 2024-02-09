
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load the data from the file
with open('cleaned_silicon_valley_crypto_news.txt', 'r') as f:
    data = f.read()

# Tokenize the data
words = word_tokenize(data)

# Remove stopwords
stop_words = set(stopwords.words('english'))
words = [word for word in words if word.lower() not in stop_words]

# Lemmatize the words
lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(word) for word in words]

# Perform sentiment analysis
sia = SentimentIntensityAnalyzer()
sentiment_scores = sia.polarity_scores(data)

# Write the results to a file
with open('sentiment_analysis_results.txt', 'w') as f:
    f.write('Sentiment Analysis Results:\n\n')
    f.write('Positive: {}\n'.format(sentiment_scores['compound'][1]))
    f.write('Negative: {}\n'.format(sentiment_scores['compound'][0]))
    f.write('Neutral: {}\n'.format(sentiment_scores['compound'][2]))

