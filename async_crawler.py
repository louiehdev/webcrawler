import asyncio
import aiohttp
from crawl import extract_page_data, normalize_url

class AsyncCrawler():
    def __init__(self, base_url, max_concurrency, max_pages):
        self.base_url = base_url
        self.base_domain = normalize_url(base_url)
        self.page_data = {}
        self.max_concurrency = max_concurrency
        self.max_pages = max_pages
        self.should_stop = False
        self.all_tasks = set()
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(self.max_concurrency)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
    
    async def add_page_visit(self, normalized_url):
        async with self.lock:
            if self.should_stop:
                return False
            if len(self.page_data) >= self.max_pages:
                self.should_stop = True
                print("Reached maximum number of pages to crawl.")
                for task in self.all_tasks:
                    task.cancel()
                return False
            return False if self.page_data.get(normalized_url) else True
    
    async def get_html(self, url):
        try:
            async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as resp:
                if resp.status > 399:
                    return None
                if 'text/html' not in resp.headers.get('content-type'):
                    return None
                return await resp.text()
        except Exception as e:
            print(f"error receiving data from {url}: {e}")
            return None

    async def crawl_page(self, current_url):
        if self.should_stop:
            return

        normalized = normalize_url(current_url)
        if not await self.add_page_visit(normalized):
            return
        if normalize_url(self.base_url) not in normalized:
            return
        async with self.semaphore:
            html = await self.get_html(current_url)
            if html is None:
                return
            page = extract_page_data(html, current_url)
            async with self.lock:
                self.page_data[normalized] = page
            print(f"crawled through {normalized}")

        tasks = []      
        for url in page.get('outgoing_links'):
            task = asyncio.create_task(self.crawl_page(url))
            tasks.append(task)
            self.all_tasks.add(task)
        if tasks:
            try:
                await asyncio.gather(*tasks, return_exceptions=True)
            finally:
                for task in tasks:
                    self.all_tasks.discard(task)
            
    
    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data

async def crawl_site_async(base_url, max_concurrency, max_pages):
    async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
        return await crawler.crawl()
