from bs4 import BeautifulSoup
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from collections import Counter

console = Console()


class DuplicateIdsParser:
    def __init__(self, file_paths):
        self.files = [Path(f) for f in file_paths]
        self.results = []

    def parse_file(self, file_path: str):
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        ids: list[str] = []

        for tag in soup.find_all(True):
            # если тег находится внутри <svg> — пропускаем
            if tag.find_parent("svg"):
                continue

            raw_id = tag.get("id")
            if isinstance(raw_id, str):
                ids.append(raw_id)

        counter: Counter[str] = Counter(ids)

        duplicates: set[str] = {id_ for id_, count in counter.items() if count > 1}

        return {
            "ids": duplicates,
            "file": str(file_path),
        }

    def parse_all(self):
        self.results = [self.parse_file(f) for f in self.files]

    def display(self):
        if not self.results:
            console.print("[yellow]No results. Run parse_all() first.[/yellow]")
            return

        for r in self.results:
            ids_str = ", ".join(r["ids"]) if r["ids"] else "None"

            table = Table(show_header=False, box=None, pad_edge=False)
            table.add_row("Ids:", ids_str)

            panel = Panel(
                table,
                title=f"[bold cyan]{r['file']}[/bold cyan]",
                expand=False,
                border_style="green",
            )
            console.print(panel)
