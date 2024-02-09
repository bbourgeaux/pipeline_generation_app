
import xml.etree.ElementTree as ET
import re

# Read silicon_valley_news.ext file
tree = ET.parse('silicon_valley_news.ext')
root = tree.getroot()

# Find all the articles in the file
articles = root.findall('article')

# Initialize headlines list
headlines = []

# Iterate through each article and extract headline
for article in articles:
    title = article.find('title').text
    date = article.find('date').text
    
    # Check if the date is today
    if re.search(r'\d{1,2}\/\w+\/\d{4}', date).group() == re.search(r'\d{1,2}\/\w+\/\d{4}', '2021-09-01').group():
        headlines.append(title)

# Write headlines to headlines.ext file
with open('headlines.ext', 'w') as f:
    for headline in headlines:
        f.write(headline + '\n')


