import unittest
from crawl import normalize_url, get_h1_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):
    def test_normalize_url(self):
        input_url = "https://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)
    
    def test_normalize_url_slash(self):
        input_url = "https://blog.boot.dev/path/"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_http(self):
        input_url = "http://blog.boot.dev/path"
        actual = normalize_url(input_url)
        expected = "blog.boot.dev/path"
        self.assertEqual(actual, expected)

class TestParser(unittest.TestCase):
    def test_get_h1(self):
        input_html = '<h1>Hello World!</h1>'
        actual = get_h1_from_html(input_html)
        expected = "Hello World!"
        self.assertEqual(actual, expected)
    
    def test_get_h1_empty(self):
        input_html = '<h1></h1>'
        actual = get_h1_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_h1_full(self):
        input_html = '''<html><body>
            <h1>Who do you think you are.</h1>
            <main>
            <p>I am.</p>
            <p>Get it right.</p>
            </main>
        </body></html>'''
        actual = get_h1_from_html(input_html)
        expected = "Who do you think you are."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html(self):
        input_body = '''<html><body>
            <p>I'm a paragraph.</p>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "I'm a paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_empty(self):
        input_body = '<html><body></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

class TestURLs(unittest.TestCase):
    def test_get_urls_from_html(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_absolute(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><a href="https://blog.boot.dev/posts"></a><a href="/posts/new"></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/posts", "https://blog.boot.dev/posts/new"]
        self.assertEqual(actual, expected)
    
    def test_get_urls_from_html_none(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="https://blog.boot.dev/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://blog.boot.dev/logo.png"]
        self.assertEqual(actual, expected)
    
    def test_get_images_from_html_none(self):
        input_url = "https://blog.boot.dev"
        input_body = '<html><body></body></html>'
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

class TestExtractPageData(unittest.TestCase):
    def test_extract_page_data_basic(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1"],
            "image_urls": ["https://blog.boot.dev/image1.jpg"]
        }
        self.assertEqual(actual, expected)
    
    def test_extract_page_data_multiple(self):
        input_url = "https://blog.boot.dev"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <img src="/image1.jpg" alt="Image 1">
            <main>
                <p>This is the main paragraph.</p>
                <img src="https://blog.boot.dev/image2.jpg" alt="Image 2">
            </main>
            <a href="/link1">Link 1</a>
            <a href="https://blog.boot.dev/link2">Link 2</a>
            <a href="https://other.boot.dev/link3">Link 3</a>
            <img src="/image3.png" alt="Image 3">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://blog.boot.dev",
            "h1": "Test Title",
            "first_paragraph": "This is the main paragraph.",
            "outgoing_links": ["https://blog.boot.dev/link1", "https://blog.boot.dev/link2", "https://other.boot.dev/link3"],
            "image_urls": ["https://blog.boot.dev/image1.jpg", "https://blog.boot.dev/image2.jpg", "https://blog.boot.dev/image3.png"]
        }
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()