from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.netloc + parsed.path.rstrip("/")

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.h1.get_text() if soup.find('h1') else ""

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.main.p.get_text() if soup.find('main') and soup.find('p') else (soup.p.get_text() if soup.find('p') else "")

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    return [url.get('href') if not url.get('href').startswith('/') else urljoin(base_url, url.get('href')) for url in soup.find_all('a')]

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    return [url.get('src') if not url.get('src').startswith('/') else urljoin(base_url, url.get('src')) for url in soup.find_all('img')]

def extract_page_data(html, page_url):
    return {"url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)}