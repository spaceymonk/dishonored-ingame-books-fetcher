from bs4 import BeautifulSoup
import requests

URL = 'https://dishonored.fandom.com/wiki/Category:Dishonored_Books'


def parse_index_page(url=URL):
    if url.startswith('http'):
        with requests.get(url) as response:
            soup = BeautifulSoup(response.text, 'html.parser')
            book_items = parse(soup)
    else:
        with open(url, 'r') as fp:
            soup = BeautifulSoup(fp, 'html.parser')
            book_items = parse(soup)
    return book_items


def parse(soup):
    book_items = []
    items = soup.select('#mw-content-text > div.category-page__members ul > li> a')
    for item in items[1:]:
        title = item['title']
        href = item['href']
        book_items.append((title, href))
    return book_items
