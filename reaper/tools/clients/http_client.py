"""Storage module for class HTTPClient"""
from typing import Optional
from requests import Response, get, post, put


class HTTPClient:
    """Class sending requests"""

    @staticmethod
    def get(url: str, headers: Optional[dict] = None, params: Optional[dict] = None) -> Response:
        return get(url, headers=headers, params=params)

    @staticmethod
    def post(url: str, headers: Optional[dict] = None, params: Optional[dict] = None, json: Optional[str] = None,
             data: Optional[dict] = None) -> Response:
        return post(url, headers=headers, params=params, json=json, data=data)

    @staticmethod
    def put(url: str, headers: Optional[dict] = None, params: Optional[dict] = None, json: Optional[str] = None,
            data: Optional[dict] = None) -> Response:
        return put(url, headers=headers, params=params, json=json, data=data)
