from flask import (
    session,
)
import json
from src import config
import requests
import os


class UserApi:

    def __init__(self):
        self.base_url = config.user_api_url
        self.headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {session.get('access_token')}"
        }

    def _make_post_request(self, endpoint, data):
        url = f"{self.base_url}/{endpoint}"
        response = requests.request("POST", url, data=json.dumps(data), headers=self.headers)
        return json.loads(response.text)

    def post_document(self, filepath, folder_id):
        endpoint = f"post_document/{folder_id}/{id}"
        with open(filepath, 'rb') as f:
            file=f.read()
        filename = os.path.basename(filepath)

        return self._make_post_request(endpoint, {'file_content':file, "file_name": filename})
