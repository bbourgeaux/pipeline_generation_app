
import requests
from bs4 import BeautifulSoup

# define the URL of the resource to be scraped
url = "https://www.siliconvalleynews.ext"

# define the response format
response_format = "html"

# send a GET request to the URL
response = requests.get(url, response_format=response_format)

# parse the HTML content of the response
soup = BeautifulSoup(response.text, "html.parser")

# find all the article links
article_links = soup.find_all("a", class_="article-link")

# define a list to store the extracted articles
extracted_articles = []

# loop through each article link
for link in article_links:
    # extract the article URL
    article_url = link["href"]
    
    # send a GET request to the article URL
    article_response = requests.get(article_url, response_format=response_format)
    
    # parse the HTML content of the article response
    article_soup = BeautifulSoup(article_response.text, "html.parser")
    
    # extract the article title and body
    article_title = article_soup.find("h2", class_="article-title").text
    article_body = article_soup.find("div", class_="article-body").text
    
    # add the extracted article to the list
    extracted_articles.append({"title": article_title, "body": article_body})

# save the extracted articles to a new resource file
with open("silicon_valley_news_extracted.ext", "w") as f:
    for article in extracted_articles:
        f.write(article["title"] + "\n")
        f.write(article["body"] + "\n")

