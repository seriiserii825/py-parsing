import requests
import xml.etree.ElementTree as ET
from rich import print

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ParserBot/1.0)"
}


class SitemapParser:
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
