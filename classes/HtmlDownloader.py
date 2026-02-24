import os
import requests
from urllib.parse import urlparse
from rich import print
from rich.progress import track

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ParserBot/1.0)"
}


class HtmlDownloader:
    def __init__(self, urls: list[str], domain: str, output_dir: str = "") -> None:
        self.urls = urls
        self.domain = domain
        self.base_dir = os.path.join(output_dir, domain)

    def download_all(self) -> None:
        os.makedirs(self.base_dir, exist_ok=True)
        failed: list[str] = []

        for url in track(self.urls, description=f"Downloading {self.domain}..."):
            filepath = self._url_to_filepath(url)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            try:
                response = requests.get(url, headers=HEADERS, timeout=15)
                response.raise_for_status()
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)
            except Exception as e:
                print(f"[red]Failed: {url} — {e}")
                failed.append(url)

        total = len(self.urls)
        done = total - len(failed)
        print(
            f"[green]Done: {done}/{total} pages saved to [bold]{self.base_dir}[/bold]")
        if failed:
            print(f"[yellow]Failed ({len(failed)}):")
            for url in failed:
                print(f"  [yellow]{url}")

    def _url_to_filepath(self, url: str) -> str:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        if not path:
            return os.path.join(self.base_dir, "index.html")
        if "." not in os.path.basename(path):
            path = os.path.join(path, "index.html")
        return os.path.join(self.base_dir, path)
