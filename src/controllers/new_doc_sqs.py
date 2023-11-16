import json
import os
from src import config
from src.utils import csv_generation
from src.utils.pdf_reader import PDFReader
from src.dependencies.openapi import DataExtractor
from src.dependencies.users_api import UserApi
from src.utils.aws_s3 import AWSService
import shutil

class NewDocSqs:
    def __init__(self, body):
        self.body = body

        if body['type'] == 'urls':
            self.process_urls()

        elif body['type'] == 'file':
            self.process_files()

    def process_urls(self):
        new_dict = {
            "website_urls": self.body['url_list'],
            "phrases_list": self.body.get('phrases_list')
        }
        extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)

        self.output_data(extracted_data, 'url')

    def process_files(self):
        _, file_extension = os.path.splitext(self.body['filename'])
        if file_extension.lower() == '.zip':
            self.process_zip()
        elif file_extension.lower() == '.csv':
            self.process_csv()
        elif file_extension.lower() == '.pdf':
            self.process_pdf()

    def process_csv(self):
        extracted_list = []
        csv_read = CSVReader().read_csv(self.body['filename'])
        
        for i in range(0, len(csv_read), 20):
            batch_urls = csv_read[i:i+20]
            new_dict = {
                "website_urls": batch_urls,
                "phrases_list": self.body.get('phrases_list')
            }
            extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)
            extracted_list.extend(extracted_data)
        
        self.output_data(extracted_list, 'url')

    def process_pdf(self):
        new_data = {
            'files': [{
                'folder_id': self.body['id'],
                'doc_name': self.body['filename']
            }],
            "phrases_list": self.body.get('phrases_list')
        }
        extracted_data =  DataExtractor().extract_data_from_pdf(new_data)
        self.output_data(extracted_data, 'pdf')

    def process_zip(self):
        filename_without_ext = self.body['filename'].split('.')[0]
        extract_location = f"/opt/src/documents/{filename_without_ext}"

        folder = AWSService().get_folder_list(self.body['id'], filename_without_ext)

        extracted_data = []
        for filename in folder:
            new_data = {
                'files': [{
                    'folder_id': self.body['id'],
                    'doc_name': filename
                }],
                "phrases_list": self.body.get('phrases_list')
            }
            extracted_data.extend(DataExtractor().extract_data_from_pdf(new_data))

        if os.path.exists(extract_location):
            os.remove(extract_location)

        self.output_data(extracted_data, 'zip')

    def output_data(self, extracted_data, header):
        if self.body.get('output_typeurl') == 'CSV':
            file_path = csv_generation.create_csv(extracted_data, header)
            UserApi(self.body).post_document(file_path, self.body['id'])

            data = {
                'extracted_data': extracted_data,
                'output_document_name': os.path.basename(file_path)
            }

            UserApi(self.body).update_extraction(self.body['id'], data)
            os.remove(file_path)
