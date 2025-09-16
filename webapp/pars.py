import requests
from bs4 import BeautifulSoup
from pprint import pprint

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
        print(type(all_news))
        all_news = all_news.find_all('li')
        result_news = []
        for news in all_news:
            title = news.find('a').text
            news_url = news.find('a')['href']
            published = news.find('time').text
            result_news.append({
                'title': title,
                'url': news_url,
                'time_published': published
            })
            # print(title)
            # print(news_url)
            # print(published)
        return result_news
    return False
    
if __name__ == '__main__':
    print()