from __future__ import annotations

import os
from typing import Any

import requests


class BackendUnavailableError(Exception):
    pass


class ApiClient:
    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = (base_url or os.getenv("API_BASE_URL", "http://localhost:5000")).rstrip("/")

    def _request(self, method: str, path: str, **kwargs) -> Any:
        try:
            response = requests.request(method, f"{self.base_url}{path}", timeout=5, **kwargs)
        except requests.RequestException as exc:
            raise BackendUnavailableError("Back-end indisponível. Verifique a URL da API.") from exc

        if response.status_code >= 400:
            try:
                message = response.json().get("error", response.text)
            except ValueError:
                message = response.text
            raise BackendUnavailableError(message)

        if response.status_code == 204:
            return None
        return response.json()

    def health(self) -> dict:
        return self._request("GET", "/api/health")

    def dashboard(self) -> dict:
        return self._request("GET", "/api/dashboard")

    def list_books(self, term: str = "") -> dict:
        return self._request("GET", "/api/books", params={"q": term})

    def get_book(self, book_id: int) -> dict:
        return self._request("GET", f"/api/books/{book_id}")

    def create_book(self, payload: dict) -> dict:
        return self._request("POST", "/api/books", json=payload)

    def delete_book(self, book_id: int) -> dict:
        return self._request("DELETE", f"/api/books/{book_id}")

    def borrow_book(self, book_id: int, borrower_name: str) -> dict:
        return self._request("POST", f"/api/books/{book_id}/borrow", json={"borrower_name": borrower_name})

    def return_book(self, book_id: int) -> dict:
        return self._request("POST", f"/api/books/{book_id}/return")
