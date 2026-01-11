from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

def normalize_url(url):
    parsed = urlparse(url)
    return parsed.netloc + parsed.path.rstrip("/")

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.h1.get_text().strip() if soup.find('h1') else ""

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.main.p.get_text().strip() if soup.find('main') and soup.find('p') else (soup.p.get_text().strip() if soup.find('p') else "")

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    return [url.get('href') if not url.get('href').startswith('/') else urljoin(base_url, url.get('href')) for url in soup.find_all('a')]

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    return [url.get('src') if not url.get('src').startswith('/') else urljoin(base_url, url.get('src')) for url in soup.find_all('img')]

def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url)}

def get_html(url):
    resp = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    resp.raise_for_status()
    if 'text/html' not in resp.headers.get('content-type'):
        raise Exception(f"incorrect content-type of kind {resp.headers.get('content-type')}")
    
    return resp.text

def crawl_page(base_url, current_url=None, page_data=None):
    normalized = normalize_url(current_url)
    if normalize_url(base_url) not in normalized:
        return
    if page_data.get(normalized):
        return
    try:
        page = extract_page_data(get_html(current_url), current_url)
        page_data[normalized] = page
        for url in page.get('outgoing_links'):
            crawl_page(base_url, url, page_data)
    except Exception as e:
        print(e)
        pass