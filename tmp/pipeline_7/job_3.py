
import re
import xml.etree.ElementTree as ET

# Read the input file
tree = ET.parse('silicon_valley_news_analysis.ext')
root = tree.getroot()

# Extract the articles
articles = root.findall('article')

# Initialize a flag to indicate if any news related to crypto was found
crypto_found = False

# Iterate through each article
for article in articles:
    # Get the article content
    content = article.find('content').text
    
    # Check if the article contains any news related to crypto
    if 'crypto' in content.lower():
        crypto_found = True
        
# Write the output file
tree.write('silicon_valley_crypto_news.ext')

# Print a message indicating if any news related to crypto was found
if crypto_found:
    print('Crypto news found!')
else:
    print('No crypto news found.')

