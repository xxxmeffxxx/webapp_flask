from bs4 import BeautifulSoup
from datetime import datetime
from webapp.news.parsers.utils import get_html, save_news
import locale
import platform
from webapp.db import News, db


if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, 'russian')
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')


def get_habr_snippets():
    url = 'https://habr.com/ru/news/'
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find('div', class_ = 'pull-down')
        all_news = all_news.find_all('div', class_ ='tm-article-snippet tm-article-snippet')
        #pprint(all_news)
        
        for news in all_news :
            try:
                title = news.find('h2').find('a', class_ = 'tm-title__link').text
                url = 'https://habr.com' + news.find('h2').find('a', class_ = 'tm-title__link')['href']
                published = news.find('a', class_ = 'tm-article-datetime-published tm-article-datetime-published_link').find('time')['title'].strip()
                #print(title, url, published)
                try:
                    published = datetime.strptime(published, '%Y-%m-%d, %H:%M')
                except (ValueError):
                    published = datetime.now()
            except:
                pass
            save_news(title, url, published)
        

def get_habr_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html(news.url)
        #print(html)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_ = 'article-formatted-body article-formatted-body article-formatted-body_version-2').decode_contents()
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()