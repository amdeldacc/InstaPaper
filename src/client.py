import requests
from requests_oauthlib import OAuth1
import urllib.parse
from typing import Optional

class InstapaperClient:
    BASE_URL = "https://www.instapaper.com/api/1.1"

    def __init__(self, consumer_key: str, consumer_secret: str):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.app_consumer = OAuth1(consumer_key, client_secret=consumer_secret)

    def authenticate(self, username: str, password: str) -> Optional[OAuth1]:
        params = {"x_auth_username": username, "x_auth_password": password}
        r = requests.post(f"{self.BASE_URL}/oauth/access_token", params=params, auth=self.app_consumer)
        if r.status_code != 200:
            return None
        qs = urllib.parse.parse_qs(r.text)
        return OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=qs["oauth_token"][0],
            resource_owner_secret=qs["oauth_token_secret"][0],
        )

    def list_bookmarks(self, oauth: OAuth1, folder_id: str = "unread", limit: int = 50, offset: int = 0, tag: Optional[str] = None) -> list:
        params = {"format": "json", "folder_id": folder_id, "limit": limit, "offset": offset}
        if tag:
            params["tag"] = tag
        r = requests.post(f"{self.BASE_URL}/bookmarks/list", params=params, auth=oauth)
        if r.status_code != 200:
            return []
        data = r.json()
        return data.get("bookmarks", []) if isinstance(data, dict) else []

    def get_text(self, oauth: OAuth1, bookmark_id: int) -> Optional[str]:
        r = requests.post(f"{self.BASE_URL}/bookmarks/get_text", params={"bookmark_id": bookmark_id}, auth=oauth)
        return r.text if r.status_code == 200 else None

    def list_folders(self, oauth: OAuth1) -> list:
        r = requests.post(f"{self.BASE_URL}/folders/list", params={"format": "json"}, auth=oauth)
        return r.json() if r.status_code == 200 else []
