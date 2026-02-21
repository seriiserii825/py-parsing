# downloader.py
import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ParserBot/1.0)"
}


def download_html(url: str) -> str:
    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )
    response.raise_for_status()
    return response.text
