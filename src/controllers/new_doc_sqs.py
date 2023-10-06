import json

from src.utils.web_scrape import WebScraper
from src.dependencies.openapi import DataExtractor


class NewDocSqs(object):
    def __init__(self, body):

        if body['type'] == 'url':
            scraped_websites = WebScraper().site_scrape(body['url_list'])

            new_dict = {
                "scraped_websites": scraped_websites,
                "phrases_list": body.get('phrases_list')
            }
            extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)
            print(extracted_data)
            if body.get('output_typeurl'):
                if body['output_typeurl'] == 'CSV':
                    print('do stuff')
