import requests
import xml.etree.ElementTree as ET
from rich import print

from classes.Select import Select

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ParserBot/1.0)"
}


class SitemapParser:
    NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    def __init__(self, sitemap_url: str) -> None:
        self.sitemap_url = sitemap_url
        self.urls: list[str] = []

    def parse(self) -> list[str]:
        root = self._fetch_xml(self.sitemap_url)
        if root is None:
            return []
        if "sitemapindex" in root.tag.lower():
            for sitemap in root.findall(f"{{{SITEMAP_NS}}}sitemap"):
                loc = sitemap.find(f"{{{SITEMAP_NS}}}loc")
                if loc is not None and loc.text:
                    sub_root = self._fetch_xml(loc.text.strip())
                    if sub_root is not None:
                        self._extract_urls(sub_root)
        else:
            self._extract_urls(root)
        return self.urls

    def parseBySelect(self) -> list[str]:
        sitemaps = self._fetch_root_sitemaps()

        if not sitemaps:
            print("[red]No sitemaps found in index")
            return []

        selected_sitemap = self._select_sitemap(sitemaps)
        if not selected_sitemap:
            return []

        print(f"\n[green]Selected sitemap:[/green] {selected_sitemap}")

        urls = self._fetch_urls_from_sitemap(selected_sitemap)
        if not urls:
            print("[red]No URLs found in sitemap")
            return []

        return self._select_urls(urls)

    def _fetch_root_sitemaps(self) -> list[str]:
        r = requests.get(self.sitemap_url, timeout=15)
        r.raise_for_status()

        root = ET.fromstring(r.text)

        return [
            loc.text.strip()
            for loc in root.findall(".//ns:sitemap/ns:loc", self.NS)
            if loc.text
        ]

    def _select_sitemap(self, sitemaps: list[str]) -> str | None:
        print("\n[bold cyan]Available sitemaps:[/bold cyan]")

        for i, sm in enumerate(sitemaps):
            print(f"[cyan][{i}][/cyan] {sm}")

        raw = input("\nSelect sitemap index: ").strip()

        if not raw.isdigit():
            print("[red]Invalid input")
            return None

        idx = int(raw)
        if idx < 0 or idx >= len(sitemaps):
            print("[red]Index out of range")
            return None

        return sitemaps[idx]

    def _fetch_urls_from_sitemap(self, sitemap_url: str) -> list[str]:
        r = requests.get(sitemap_url, timeout=15)
        r.raise_for_status()

        root = ET.fromstring(r.text)

        return [
            loc.text.strip()
            for loc in root.findall(".//ns:url/ns:loc", self.NS)
            if loc.text
        ]

    def _select_urls(self, urls: list[str]) -> list[str]:
        for i, url in enumerate(urls):
            print(f"[cyan][{i}][/cyan] {url}")

        raw = input(
            "\nSelect URLs (1 | 1,3 | 0-5 | a=all): "
        ).strip()

        if raw.lower() == "a":
            return urls

        indexes: list[int]

        if "," in raw:
            indexes = [int(i) for i in raw.split(",")]

        elif "-" in raw:
            start, end = map(int, raw.split("-", 1))
            indexes = list(range(start, end + 1))  # 🔥 ВАЖНО

        else:
            indexes = [int(raw)]

        return [
            urls[i]
            for i in indexes
            if 0 <= i < len(urls)
        ]

    def _fetch_xml(self, url: str) -> ET.Element | None:
        try:
            response = requests.get(url, headers=HEADERS, timeout=15)
            response.raise_for_status()
            return ET.fromstring(response.content)
        except requests.RequestException as e:
            print(f"[red]Failed to fetch sitemap: {url} — {e}")
            return None
        except ET.ParseError as e:
            print(f"[red]Failed to parse XML: {url} — {e}")
            return None

    def _extract_urls(self, root: ET.Element) -> None:
        for url_el in root.findall(f"{{{SITEMAP_NS}}}url"):
            loc = url_el.find(f"{{{SITEMAP_NS}}}loc")
            if loc is not None and loc.text:
                self.urls.append(loc.text.strip())
