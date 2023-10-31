import json
import os
import zipfile
import time
from src import config
from src.utils import csv_generation
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
        new_dict = {
            "website_urls": self.body['url_list'],
            "phrases_list": self.body.get('phrases_list')
        }
        extracted_data = DataExtractor().extract_data_from_webscraped_urls(new_dict)

        self.output_data(extracted_data, 'url')

    def process_files(self):
        _, file_extension = os.path.splitext(self.body['filename'])

        # if file_extension.lower() == '.zip':
        #     self.process_zip()
        if file_extension.lower() == '.csv':
            self.process_csv()
        elif file_extension.lower() == '.pdf':
            self.process_pdf()

        # summary_doc = DataExtractor().create_summary_report(self.output_data)

        # if os.path.exists(f"/opt/src/documents/{self.body['filename']}"):
        #     os.remove(f"/opt/src/documents/{self.body['filename']}")

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
        self.output_data(extracted_data, 'file name')


    # def process_zip(self):
    #     filename_without_ext = self.body['filename'].split('.')[0]
    #     extract_to = f"/opt/src/documents/{filename_without_ext}"
    #     with zipfile.ZipFile(f"/opt/src/documents/{self.body['filename']}", 'r') as zip_ref:
    #         zip_ref.extractall(extract_to)

    #     time.sleep(5)

    #     extracted_data_list = []
    #     for foldername, subfolders, filenames in os.walk(extract_to):
    #         for filename in filenames:
    #             file_path = os.path.join(foldername, filename)
                
    #             if filename.lower().endswith('.pdf'):
    #                 extracted_data = self.process_pdf(file_path)
    #             elif filename.lower().endswith('.csv'):
    #                 extracted_data = self.process_csv(file_path)
    #             extracted_data_list.append(extracted_data)
    #     return extracted_data_list


    def output_data(self, extracted_data, header):
        if self.body.get('output_typeurl') == 'CSV':
            print(extracted_data)
            file_path = csv_generation.create_csv(extracted_data, header)
            UserApi(self.body).post_document(file_path, self.body['id'])

            data = {
                'extracted_data': extracted_data,
                'output_document_name': os.path.basename(file_path)
            }

            UserApi(self.body).update_extraction(self.body['id'], data)
            os.remove(file_path)
