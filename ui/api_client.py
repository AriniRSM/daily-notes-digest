from datetime import date

import requests


API_BASE_URL = "http://127.0.0.1:8000"


def _raise_for_api_error(response: requests.Response):
    try:
        detail = response.json().get("detail")
    except ValueError:
        detail = response.text

    if detail:
        raise RuntimeError(detail)

    response.raise_for_status()


def create_item(raw_input: str):
    response = requests.post(
        f"{API_BASE_URL}/items",
        json={"raw_input": raw_input},
        timeout=10,
    )
    if not response.ok:
        _raise_for_api_error(response)
    return response.json()


def list_items():
    response = requests.get(f"{API_BASE_URL}/items", timeout=10)
    if not response.ok:
        _raise_for_api_error(response)
    return response.json()


def generate_today_digest(target_date: date | None = None):
    try:
        params = {"target_date": target_date.isoformat()} if target_date else None
        response = requests.post(
            f"{API_BASE_URL}/digest/today",
            params=params,
            timeout=150,
        )
        if not response.ok:
            _raise_for_api_error(response)

        return response.json()
    except requests.ConnectionError:
        raise RuntimeError("Backend API is not running. Start FastAPI first.")
    except requests.Timeout:
        raise RuntimeError("Digest generation timed out.")


def get_digest_data():
    try:
        response = requests.get(
            f"{API_BASE_URL}/digest/data",
            timeout=10,
        )

        if response.status_code == 404:
            return None

        if not response.ok:
            _raise_for_api_error(response)

        return response.json()
    except requests.ConnectionError:
        raise RuntimeError("Backend API is not running. Start FastAPI first.")
    except requests.Timeout:
        raise RuntimeError("Digest fetch timed out.")
