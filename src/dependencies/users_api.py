from flask import (
    session,
)
import json
from src import config
import requests
import os


class UserApi:

    def __init__(self, body):
        self.base_url = config.user_api_url
        self.access_token = body.get('access_token')
        self.headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {body.get('access_token')}"
        }

    def _make_post_request_files(self, endpoint, files):
        url = f"{self.base_url}/{endpoint}"
        headers = {'Authorization': f"Bearer {self.access_token}"}
        response = requests.post(url, files=files, headers=headers)
        return json.loads(response.text)

    def _make_post_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, data=json.dumps(data), headers=self.headers)
        return json.loads(response.text)

    def _make_get_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, data=json.dumps(data), headers=self.headers)
        return json.loads(response.text)


    def post_document(self, filepath, folder_id):
        endpoint = f"post_document/{folder_id}"
        with open(filepath, 'rb') as file:
            files = {os.path.basename(filepath): file}
            return self._make_post_request_files(endpoint, files)

    def update_extraction(self, folder_id, data):
        endpoint = f"update_extraction/{folder_id}"
        return self._make_post_request(endpoint, data)

    def get_document_extract(self, folder_id, data):
        endpoint = f"update_extraction/{folder_id}"
        return self._make_get_request(endpoint, data)

