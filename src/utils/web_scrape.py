import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self):
        self.websites_content = {}

    def site_scrape(self, urls_list):
        for url in urls_list:
            cleaned = self.fetch_and_clean_html(url)
            self.websites_content[url] = cleaned
        return self.websites_content

    def fetch_and_clean_html(self, url):
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove all script tags
            for script_tag in soup.find_all('script'):
                script_tag.decompose()
            
            # Remove all style tags
            for style_tag in soup.find_all('style'):
                style_tag.decompose()
            
            # Remove all headers
            for header_tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header']):
                header_tag.decompose()

            # Further decompositions can be added as per requirement
            # ...

            # Extract text content
            text_content = soup.get_text(separator=' ', strip=True)

            return text_content
        
        except requests.RequestException as e:
            print(f"Error fetching content from {url}: {e}")
            return ""

    def fetch_content(self, url):
        try:
            response = requests.get(url, verify=False)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching content from {url}: {e}")
            return ""
