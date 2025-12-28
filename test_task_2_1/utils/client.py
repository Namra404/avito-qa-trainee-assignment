import os
import requests
from dotenv import load_dotenv

load_dotenv()


class ApiClient:
    """Клиент для запросов"""

    def __init__(self):
        base_url = os.getenv("BASE_URL")
        if not base_url:
            raise RuntimeError("Set BASE_URL in .env")

        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
        })

    def get(self, path: str):
        return self.session.get(f"{self.base_url}{path}")

    def post(self, path: str, json_body=None):
        if json_body is None:
            return self.session.post(f"{self.base_url}{path}", headers={"Content-Type": "application/json"})
        return self.session.post(f"{self.base_url}{path}", json=json_body)

    def delete(self, path: str):
        return self.session.delete(f"{self.base_url}{path}")
