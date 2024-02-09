import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
import os

def clean_text(text):
    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    text = re.sub(r'\d+', '', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Tokenize the text
    words = word_tokenize(text)
    
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    
    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Join the words back into a string
    text = ' '.join(words)
    
    return text

def preprocess_news_data(input_file, output_file):
    with open(input_file, 'r') as f:
        text = f.read()
        
    # Clean the text
    text = clean_text(text)
    
    # Write the preprocessed text to a new file
    with open(output_file, 'w') as f:
        f.write(text)

# Call the function with the input and output files
preprocess_news_data('silicon_valley_news.txt', 'preprocessed_news_data.txt')
