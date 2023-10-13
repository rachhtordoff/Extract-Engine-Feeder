import json
import os
import zipfile

from src import config
from src.utils import csv_generation
from src.utils.web_scrape import WebScraper
from src.utils.pdf_reader import PDFReader
from src.dependencies.openapi import DataExtractor
from src.dependencies.users_api import UserApi
from src.utils.aws_s3 import AWSService


class NewDocSqs:
    def __init__(self, body):
        self.body = body

        if body['type'] == 'urls':
            self.process_urls()

        elif body['type'] == 'file':
            self.process_files()

    def process_urls(self):
        scraped_websites = WebScraper().site_scrape(self.body['url_list'])
        new_dict = {
            "scraped_websites": scraped_websites,
            "phrases_list": self.body.get('phrases_list')
        }
        extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)
        self.output_data(extracted_data)

    def process_files(self):
        AWSService().download_file(self.body['id'], self.body['filename'])
        _, file_extension = os.path.splitext(self.body['filename'])

        if file_extension.lower() == '.pdf':
            extracted_data = self.process_pdf()
        elif file_extension.lower() == '.zip':
            extracted_data = self.process_zip()
        elif file_extension.lower() == '.csv':
            extracted_data = self.process_csv()
        self.output_data(extracted_data)
        os.remove(f"{config.doc_location}{self.body['filename']}")

    def process_csv(self):
        extracted_list = []
        csv_read = CSVReader().read_csv(self.body['filename'])
        
        for i in range(0, len(csv_read), 20):
            batch_urls = csv_read[i:i+20]
            scraped_websites = [WebScraper().site_scrape(url) for url in batch_urls]
            new_dict = {
                "scraped_websites": scraped_websites,
                "phrases_list": self.body.get('phrases_list')
            }
            extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)
            extracted_list.extend(extracted_data)
        
        self.output_data(extracted_list)

    def process_pdf(self):
        pdf_read = PDFReader().read_pdf(self.body['filename'])
        new_data = {
            "phrases_list": self.body.get('phrases_list'),
            "pdf_data": {self.body['filename']: pdf_read}
        }
        return DataExtractor().extract_data_from_pdf(new_data)

    def process_zip(self):
        with zipfile.ZipFile(self.body['filename'], 'r') as zip_ref:
            zip_ref.extractall(f'{config.doc_location}/{self.body["filename"]}')

        for foldername, subfolders, filenames in os.walk(f'{config.doc_location}/{self.body["filename"]}'):
            for filename in filenames:
                if filename.lower().endswith('.pdf'):
                    return self.process_pdf()
                elif filename.lower().endswith('.csv'):
                    return self.process_csv()


    def output_data(self, extracted_data):
        if self.body.get('output_typeurl') == 'CSV':
            file_path = csv_generation.create_csv(extracted_data, 'urls')
            UserApi(self.body).post_document(file_path, self.body['id'])

            data = {
                'extracted_data': extracted_data,
                'output_document_name': os.path.basename(file_path)
            }

            UserApi(self.body).update_extraction(self.body['id'], data)
            os.remove(file_path)
