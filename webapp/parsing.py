import requests
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime
from webapp.model import db, News 


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False
    
def get_python_news():
    url = 'https://www.python.org/blogs/'
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('ul', class_ = 'list-recent-posts menu')
        #print(type(all_news))
        all_news = all_news.find_all('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            url = news.find('a')['href']
            published = news.find('time').text.strip()
            print(published)
            try:
                published = datetime.strptime(published, '%b. %d, %Y')
            except (ValueError):
                published = datetime.now()
            save_news(title, url, published)
    

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()
    if not news_exists:
        new_news = News(title=title, url=url, published=published)
        db.session.add(new_news)
        db.session.commit()


if __name__ == '__main__':
    print()