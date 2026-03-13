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
        self.ids: set[str] = set()  # для проверки дубликатов id на странице

    def parse_file(self, file_path: Path) -> List[LinkInfo]:
        """Парсит один файл и возвращает список ссылок с метаданными"""
        local_links = []

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Ошибка чтения {file_path.name}: {e}[/red]")
            return []

        soup = BeautifulSoup(content, "html.parser")

        for id_tag in soup.find_all(attrs={"id": True}):
            id_value = id_tag["id"]
            self.ids.add(str(id_value))

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
                and ("whatsapp" in str(link.href).lower()
                     or "wa.me" in str(link.href).lower())
            ]
            self.all_links.extend(whatsapp_links)

    def parse_hash_no_ids(self) -> None:
        """Парсит все файлы и сохраняет только ссылки с href='#' и без id"""
        self.all_links.clear()

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")
            links = self.parse_file(path)
            hash_links = [
                link for link in links if link.href and '#' in str(link.href)
            ]

            ids_from_hash_links = [
                link.href.split('#', 1)[1]
                for link in hash_links
                if link.href.split('#', 1)[1]
            ]

            for hash_id in ids_from_hash_links:
                if hash_id not in self.ids:
                    self.all_links.extend(
                        [link for link in hash_links if link.href and hash_id in str(
                            link.href)]
                    )

    def parse_role_button(self) -> None:
        """Парсит все файлы и сохраняет элементы с role на не-div/span тегах"""
        self.all_links.clear()

        allowed_tags = {"div", "span"}

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")

            try:
                content = path.read_text(encoding="utf-8")
            except Exception as e:
                console.print(f"[red]Ошибка чтения {path.name}: {e}[/red]")
                continue

            soup = BeautifulSoup(content, "html.parser")

            for tag in soup.find_all(attrs={"role": True}):
                if tag.name in allowed_tags:
                    continue

                line_number = self._get_line_number(tag, content)
                id_attr = tag.get("id")

                link = LinkInfo(
                    filename=path.name,
                    line_number=line_number,
                    href=str(tag.name),           # tag name, e.g. "h2", "button"
                    text=tag.get_text(strip=True),
                    id_attr=str(id_attr) if id_attr else None,
                    class_attr=str(tag.get("class")),
                    title_attr=str(tag.get("role")),  # role value
                )
                self.all_links.append(link)

    def parse_aria_hidden_focusable(self) -> None:
        """Находит focusable элементы внутри aria-hidden=true — они скрыты от AT, но доступны с клавиатуры"""
        self.all_links.clear()

        focusable_tags = {"a", "button", "input", "select", "textarea"}

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")

            try:
                content = path.read_text(encoding="utf-8")
            except Exception as e:
                console.print(f"[red]Ошибка чтения {path.name}: {e}[/red]")
                continue

            soup = BeautifulSoup(content, "html.parser")

            for hidden in soup.find_all(attrs={"aria-hidden": "true"}):
                for child in hidden.find_all(True):
                    tag_name = child.name
                    is_focusable_tag = tag_name in focusable_tags
                    has_href = tag_name == "a" and child.get("href")
                    tabindex = child.get("tabindex")
                    has_tabindex = tabindex is not None and str(tabindex) != "-1"

                    if (is_focusable_tag and (tag_name != "a" or has_href)) or has_tabindex:
                        line_number = self._get_line_number(child, content)
                        id_attr = child.get("id")

                        link = LinkInfo(
                            filename=path.name,
                            line_number=line_number,
                            href=str(tag_name),          # focusable tag name
                            text=child.get_text(strip=True),
                            id_attr=str(id_attr) if id_attr else None,
                            class_attr=str(child.get("class")),
                            title_attr=str(hidden.name),  # aria-hidden parent tag
                        )
                        self.all_links.append(link)

    def show_aria_hidden_results(self) -> None:
        """Выводит таблицу focusable элементов внутри aria-hidden=true"""
        if not self.all_links:
            console.print("[bold yellow]Проблем не найдено[/bold yellow]")
            return

        table = Table(
            title="Focusable элементы внутри aria-hidden=\"true\"",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Файл", style="cyan", no_wrap=True)
        table.add_column("Строка", justify="right")
        table.add_column("Тег", style="red")
        table.add_column("Родитель", style="yellow")
        table.add_column("Текст", style="white")
        table.add_column("id", style="blue")
        table.add_column("class", style="dim")

        for link in self.all_links:
            classes = (
                " ".join(link.class_attr)
                if isinstance(link.class_attr, list)
                else link.class_attr or ""
            )
            table.add_row(
                link.filename,
                str(link.line_number),
                link.href,           # focusable tag
                link.title_attr or "",  # aria-hidden parent
                link.text[:60] + ("..." if len(link.text) > 60 else ""),
                link.id_attr or "",
                classes,
            )

        console.print(table)

    def show_role_results(self) -> None:
        """Выводит таблицу элементов с role на неподходящих тегах"""
        if not self.all_links:
            console.print("[bold yellow]Элементов с некорректным role не найдено[/bold yellow]")
            return

        table = Table(
            title="Role на неподходящих тегах (не div/span)",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Файл", style="cyan", no_wrap=True)
        table.add_column("Строка", justify="right")
        table.add_column("Тег", style="red")
        table.add_column("role", style="yellow")
        table.add_column("Текст", style="white")
        table.add_column("id", style="blue")
        table.add_column("class", style="dim")

        for link in self.all_links:
            classes = (
                " ".join(link.class_attr)
                if isinstance(link.class_attr, list)
                else link.class_attr or ""
            )
            table.add_row(
                link.filename,
                str(link.line_number),
                link.href,          # tag name
                link.title_attr or "",  # role value
                link.text[:60] + ("..." if len(link.text) > 60 else ""),
                link.id_attr or "",
                classes,
            )

        console.print(table)

    def parse_img_no_alt_role(self) -> None:
        """Находит <img> без alt или с пустым alt, у которых нет role="presentation"/"none" """
        self.all_links.clear()

        for path in self.files:
            if not path.is_file():
                console.print(f"[yellow]Пропуск: {path} — не файл[/yellow]")
                continue

            console.print(f"[dim]Обработка: {path.name}[/dim]")

            try:
                content = path.read_text(encoding="utf-8")
            except Exception as e:
                console.print(f"[red]Ошибка чтения {path.name}: {e}[/red]")
                continue

            soup = BeautifulSoup(content, "html.parser")

            for img in soup.find_all("img"):
                alt = img.get("alt")
                missing_or_empty_alt = alt is None or str(alt).strip() == ""
                if not missing_or_empty_alt:
                    continue

                role = str(img.get("role", "")).strip().lower()
                if role in ("presentation", "none"):
                    continue

                line_number = self._get_line_number(img, content)
                id_attr = img.get("id")

                link = LinkInfo(
                    filename=path.name,
                    line_number=line_number,
                    href=str(img.get("src", "")),
                    text="(no alt)" if alt is None else "(empty alt)",
                    id_attr=str(id_attr) if id_attr else None,
                    class_attr=str(img.get("class")),
                    title_attr=role or "(no role)",
                )
                self.all_links.append(link)

    def show_img_no_alt_role_results(self) -> None:
        """Выводит таблицу img без alt и без role=presentation"""
        if not self.all_links:
            console.print("[bold yellow]Проблем не найдено[/bold yellow]")
            return

        table = Table(
            title='<img> без alt — требуется role="presentation"',
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Файл", style="cyan", no_wrap=True)
        table.add_column("Строка", justify="right")
        table.add_column("src", style="green")
        table.add_column("alt", style="red")
        table.add_column("role", style="yellow")
        table.add_column("id", style="blue")
        table.add_column("class", style="dim")

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
                link.text,
                link.title_attr or "",
                link.id_attr or "",
                classes,
            )

        console.print(table)

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
