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
        self.headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {body.get('access_token')}"
        }

    def _make_post_request_files(self, endpoint, files, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request("POST", url, files=files, data=json.dumps(data), headers=self.headers)
        return json.loads(response.text)

    def post_document(self, filepath, folder_id, data):
        endpoint = f"post_document/{folder_id}"
        with open(filepath, 'rb') as file:
            files = {'file': file}
            data.update({'output_document_name': os.path.basename(filepath)})

            return self._make_post_request_files(endpoint, files, data)
