import json
import os
from src.utils.web_scrape import WebScraper
from src.dependencies.openapi import DataExtractor
from src.utils import csv_generation
from src.dependencies.users_api import UserApi

class NewDocSqs(object):
    def __init__(self, body):
        print(body)
        if body['type'] == 'urls':
            scraped_websites = WebScraper().site_scrape(body['url_list'])

            new_dict = {
                "scraped_websites": scraped_websites,
                "phrases_list": body.get('phrases_list')
            }
            extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)
            if body.get('output_typeurl'):
                if body['output_typeurl'] == 'CSV':
                    file_path = csv_generation.create_csv(extracted_data, 'urls')
                    UserApi().upload_doc(file_path, body['id'])
                    os.remove(file_path)
                    