
import re
import string
import os
import sys

def clean_text(text):
    """
    This function cleans the text by removing special characters, numbers, and punctuation marks.
    """
    # Remove special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    # Remove punctuation marks
    text = re.sub(r'[^\w\.\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove stop words
    stop_words = set(string.punctuation)
    text = ' '.join([word for word in text.split() if not word in stop_words])
    return text

def preprocess_text(text):
    """
    This function preprocesses the text by removing stop words and creating a new text that contains only the important words.
    """
    # Split the text into words
    words = text.split()
    # Remove stop words
    stop_words = set(string.punctuation)
    words = [word for word in words if not word in stop_words]
    # Join the words back into a string
    text = ' '.join(words)
    return text

def clean_file(file_path):
    """
    This function cleans the file by removing special characters, numbers, and punctuation marks.
    """
    with open(file_path, 'r') as f:
        text = f.read()
        text = clean_text(text)
        f.close()
        os.remove(file_path)
        os.rename('cleaned_' + file_path, 'cleaned_silicon_valley_crypto_news.txt')

# Clean the input file
clean_file('silicon_valley_crypto_news.txt')

# Preprocess the cleaned file
with open('cleaned_silicon_valley_crypto_news.txt', 'r') as f:
    text = f.read()
    text = preprocess_text(text)
    f.close()

# Print the preprocessed text
print(text)

