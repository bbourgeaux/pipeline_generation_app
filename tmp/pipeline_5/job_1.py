import requests

url = 'https://newsapi.org/v2/top-headlines?country=us&q=silicon%20valley%20news'

response = requests.get(url)

data = response.json()

articles = data['articles']

for article in articles:
    title = article['title']
    url = article['url']
    response = requests.get(url)
    text = response.text
    with open('silicon_valley_news.txt', 'a') as f:
        f.write(title + '\n')
        f.write(text + '\n')

