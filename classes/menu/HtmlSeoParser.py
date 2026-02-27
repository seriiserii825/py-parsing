from bs4 import BeautifulSoup
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class HtmlSeoParser:
    def __init__(self, file_paths):
        self.files = [Path(f) for f in file_paths]
        self.results = []

    def parse_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else "[red]Missing"

        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = (
            meta_desc["content"]
            if meta_desc and meta_desc.get("content")
            else "[red]Missing"
        )

        og_image = soup.find("meta", attrs={"property": "og:image"})
        og_image_url = (
            og_image["content"]
            if og_image and og_image.get("content")
            else "[red]Missing"
        )

        return {
            "file": str(file_path),
            "title": title,
            "description": description,
            "og_image": og_image_url,
            "h1": self._get_headings(soup, "h1"),
            "h2": self._get_headings(soup, "h2"),
            "h3": self._get_headings(soup, "h3"),
        }

    def parse_all(self):
        self.results = [self.parse_file(f) for f in self.files]

    def display(self):
        if not self.results:
            console.print(
                "[yellow]No results. Run parse_all() first.[/yellow]")
            return

        for r in self.results:
            table = Table(show_header=False, box=None, pad_edge=False)
            table.add_row("Title:", r["title"])
            table.add_row("Description:", r["description"])
            table.add_row("OG Image:", r["og_image"])
            table.add_row("H1:", r['h1'] if r["h1"] else "[red]None")
            table.add_row("H2:", r['h2'] if r["h2"] else "[red]None")
            table.add_row("H3:", r['h3'] if r["h3"] else "[red]None")

            panel = Panel(
                table,
                title=f"[bold cyan]{r['file']}[/bold cyan]",
                expand=False,
                border_style="green",
            )
            console.print(panel)

    def _get_headings(self, soup, tag):
        tag_all = [h.text.strip() for h in soup.find_all(tag)]
        tag_count = len(tag_all)
        if tag_count == 0:
            return "[red] Missing"
        return f"({tag_count}) - {tag_all}"
