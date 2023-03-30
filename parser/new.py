import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime



URL = "https://www.securitylab.ru/news/"
HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
}


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def get_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_="article-card inline-card")
    news = []
    for it in items:
        date_from_html = it.find('time').get('datetime')
        date = datetime.datetime.strptime(date_from_html, "%Y-%m-%dT%H:%M:%S%z")
        news.append({
            "title": it.find('h2').string,
            "link": f"https://www.securitylab.ru{it.get('href')}",
            "description": it.find('p').string,
            "date_from_html": it.find('time').string,
            "date_python": date
        })
    return news


def parser():
    html = get_html(URL)
    if html.status_code == 200:
        news = []
        for i in range(1, 2):
            html = get_html(f"{URL}page1_{i}.php")
            current_page = get_data(html.text)
            news.extend(current_page)
        return news
    else:
        raise Exception("Error in parser!")