from rich import print


class SiteUrlsFile:
    def __init__(self, file_path):
        self.file_path = file_path
        self.urls = []

    def load_urls(self):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    url = line.strip()
                    if url:
                        self.urls.append(url)
        except FileNotFoundError:
            print(f"[red]File not found: {self.file_path}")
        except Exception as e:
            print(f"[red]An error occurred while loading URLs: {e}")

    def get_urls(self):
        return self.urls

    def add_url(self, url):
        url = url.strip()
        if url and url not in self.urls:
            self.urls.append(url)
            self.save_urls()
            print(f"[blue]URL added: {url}")
        else:
            print("[red]URL is empty or already exists.")

    def save_urls(self):
        try:
            with open(self.file_path, 'w') as file:
                for url in self.urls:
                    file.write(url + '\n')
        except Exception as e:
            print(f"[red]An error occurred while saving URLs: {e}")
