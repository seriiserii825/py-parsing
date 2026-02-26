from __future__ import annotations
from pathlib import Path
from typing import List, Optional, NamedTuple
from bs4 import BeautifulSoup, Tag
from rich.console import Console
from rich.table import Table


console = Console()


class LinkInfo(NamedTuple):
    """Структура данных для одной найденной ссылки"""

    filename: str
    line_number: int  # номер строки в исходном HTML
    href: str
    text: str  # текст внутри <a>...</a>
    id_attr: Optional[str] = None
    class_attr: Optional[str] = None  # или можно List[str]
    title_attr: Optional[str] = None


class HtmlLinksParser:
    def __init__(self, file_paths: List[str]):
        self.files = [Path(f) for f in file_paths]
        self.all_links: List[LinkInfo] = []

    def parse_file(self, file_path: Path) -> List[LinkInfo]:
        """Парсит один файл и возвращает список ссылок с метаданными"""
        local_links = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Ошибка чтения {file_path.name}: {e}[/red]")
            return []

        soup = BeautifulSoup(content, "html.parser")

        # Находим все теги <a>
        for a_tag in soup.find_all("a"):
            href = a_tag.get("href")
            if href is None:
                continue

            # Получаем номер строки (примерно)
            line_number = self._get_line_number(a_tag, content)
            id_attr = a_tag.get("id")

            link = LinkInfo(
                filename=file_path.name,
                line_number=line_number,
                href=str(href),
                text=a_tag.get_text(strip=True),
                id_attr=str(id_attr),
                class_attr=str(a_tag.get("class")),  # будет список или None
                title_attr=str(a_tag.get("title")),
            )
            local_links.append(link)

        return local_links

    def _get_line_number(self, tag: Tag, full_content: str) -> int:
        """
        Очень приблизительно определяет номер строки тега.
        Не идеально, но часто достаточно точно.
        """
        # Простой способ — ищем начало тега в исходном тексте
        try:
            tag_str = str(tag)[:100]  # обрезаем, чтобы не искать огромный тег
            index = full_content.index(tag_str)
            head = full_content[:index]
            return head.count("\n") + 1
        except ValueError:
            return -1  # не нашли → неизвестно

    def parse_all(self) -> None:
        """Парсит все переданные файлы"""
        self.all_links.clear()

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")
            links = self.parse_file(path)
            self.all_links.extend(links)

    def parse_empty_links(self) -> None:
        """Парсит все файлы и сохраняет только ссылки с пустым href"""
        self.all_links.clear()

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")
            links = self.parse_file(path)
            # if href are empty or have just a # hash
            empty_links = [
                link
                for link in links
                if link.href is None
                or (isinstance(link.href, str) and link.href.strip() in ("", "#"))
            ]
            self.all_links.extend(empty_links)

    def show_results(self) -> None:
        """Выводит красивую таблицу со всеми найденными ссылками"""
        if not self.all_links:
            console.print("[bold yellow]Ссылок не найдено[/bold yellow]")
            return

        table = Table(
            title="Найденные ссылки", show_header=True, header_style="bold magenta"
        )
        table.add_column("Файл", style="cyan", no_wrap=True)
        table.add_column("Строка", justify="right")
        table.add_column("href", style="green")
        table.add_column("Текст", style="white")
        table.add_column("id", style="blue")
        table.add_column("class", style="yellow")

        for link in self.all_links:
            classes = (
                " ".join(link.class_attr)
                if isinstance(link.class_attr, list)
                else link.class_attr or ""
            )
            table.add_row(
                link.filename,
                str(link.line_number),
                link.href,
                link.text[:60] + ("..." if len(link.text) > 60 else ""),
                link.id_attr or "",
                classes,
            )

        console.print(table)

    def parse_whatsap(self) -> None:
        """Парсит все файлы и сохраняет только ссылки, содержащие 'whatsapp'"""
        self.all_links.clear()

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")
            links = self.parse_file(path)
            whatsapp_links = [
                link
                for link in links
                if link.href
                and "whatsapp" in str(link.href).lower()
                or "wa.me" in str(link.href).lower()
            ]
            self.all_links.extend(whatsapp_links)
