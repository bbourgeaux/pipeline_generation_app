
import requests
from bs4 import BeautifulSoup

# Function to extract news articles from a given URL
def extract_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    articles = []
    
    for article in soup.find_all('article'):
        title = article.find('h2').text.strip()
        link = article.find('a')['href']
        articles.append((title, link))
        
    return articles

# Function to collect news articles from multiple URLs
def collect_articles(urls):
    articles = []
    
    for url in urls:
        articles += extract_articles(url)
        
    return articles

# Main function to execute the script
def main():
    urls = ['https://www.siliconvalleybusinessjournal.com/news/2021/01/13/crypto-news-and-insights-from-silicon-valley/',
            'https://www.businessinsider.com/crypto-news-silicon-valley-2021-10',
            'https://www.forbes.com/sites/forbestechcouncil/2021/09/22/the-top-crypto-news-and-resources-for-silicon-valley-tech-professionals/?sh=720c91f17f2c']
    articles = collect_articles(urls)
    
    # Print the list of articles
    print('News Collection:')
    for i, (title, link) in enumerate(articles):
        print(f'{i+1}. {title} - {link}')

# Execute the main function
if __name__ == '__main__':
    main()

