from app.api_clients.base_client import BaseHTTPClient


class UsersClient(BaseHTTPClient):
    def __init__(self, base_url: str):
        super().__init__(base_url)
