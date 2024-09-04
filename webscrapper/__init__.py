import json
import re

import requests
from bs4 import BeautifulSoup


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"


class WebScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def fetch_page(self, path=""):
        url = self.base_url + path
        try:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
                "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Referer": "https://www.dofus.com/fr",
                "DNT": "1",
            }
            response = self.session.get(url, headers=header)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page : {e}")
            return None

    def parse_html(self, html):
        return BeautifulSoup(html, "html.parser")

    def extract_data(self, soup):
        raise NotImplementedError("Subclasses should implement this method")


class DofScraper(WebScraper):
    def extract_table(self, soup):
        """Fetch table on the page"""
        table = soup.find("table", class_="ak-table ak-responsivetable")
        if table:
            tbody = table.find("tbody")
            if tbody:
                return tbody.find_all("tr")
        print(
            f"\n[{Colors.GREEN}>{Colors.RESET}] {Colors.GREEN}Rien sur cette page, traitement de la catégorie terminé.{Colors.RESET}\n"
        )
        return None

    def extract_links(self, row):
        """Get item link"""
        links = row.find_all("a", href=True)
        if not links:
            return None
        return links[1]["href"] if len(links) > 1 else links[0]["href"]

    def extract_name(self, row):
        """Get item name"""
        links = row.find_all("a", href=True)
        if not links:
            return None
        return links[1].text.strip() if len(links) > 1 else links[0].text.strip()

    def extract_type(self, row):
        """Get item type"""
        type_tag = row.find("td", class_="item-type")
        if not type_tag:
            return None
        return type_tag.text.strip()

    def extract_level(self, row):
        """Get item level"""
        level = row.find("td", class_="item-level")
        if level:
            match = re.search(r"Niv\. (\d+)", level.text.strip()) if level else None
            return match.group(1) if match else None
        return None

    def fetch_item_page(self, item_url):
        """Fetch item page"""
        html_page = self.fetch_page(item_url)
        if html_page:
            return self.parse_html(html_page)
        return None

    def extract_illus_link(self, item_url):
        """Get item illustration link"""
        soup = self.fetch_item_page(item_url)
        if soup:
            encyclo_illus = soup.find("img", class_="img-maxresponsive")
            if encyclo_illus and encyclo_illus.has_attr("src"):
                return encyclo_illus["src"] if encyclo_illus else None
        return None

    def extract_item_family(self, item_url):
        """Extract family if monster"""
        soup = self.fetch_item_page(item_url)
        if soup:
            div = soup.find("div", class_="col-xs-8 ak-encyclo-detail-type")
            if div:
                span = div.find("span")
                if span:
                    family = span.text.strip()
                    return family if div else None
        return None

    def extract_item_data(self, row):
        """Extract all item info"""
        """Put everything into a dictionary"""
        item_link = self.extract_links(row)
        item_data = {
            "link": item_link,
            "name": self.extract_name(row),
            "type": self.extract_type(row),
            "level": self.extract_level(row),
            "picture": (self.extract_illus_link(item_link)),
            "family": (self.extract_item_family(item_link)),
        }

        print(
            f"Lien : {item_data['link']} | "
            f"Nom : {item_data['name']} | "
            f"Type : {item_data['type']} | "
            f"Niveau : {item_data['level']} | "
            f"Famille : {item_data['family']} "
        )

        if all(item_data.values()):
            return item_data
        return None

    def process_items(self, _url):
        items = []
        page = 1

        while True:
            url = f"{_url}?page={page}"
            print(
                f"{Colors.BLUE}::{Colors.RESET} {Colors.YELLOW}Scraping page : {Colors.CYAN}{url}{Colors.RESET}"
            )

            html = self.fetch_page(url)
            if not html:
                break

            soup = self.parse_html(html)
            rows = self.extract_table(soup)

            if not rows:
                break

            for row in rows:
                item_info = self.extract_item_data(row)
                if item_info:
                    items.append(item_info)

            page += 1

        return items

    def scrape(self, urls, index=None):

        all_data = []

        if index is not None:
            urls = [urls[index]]

        for url in urls:
            all_data.append(self.process_items(url))
        return all_data


urls = [
    "/fr/mmorpg/encyclopedie/armes",
    "/fr/mmorpg/encyclopedie/equipements",
    "/fr/mmorpg/encyclopedie/monstres",
    "/fr/mmorpg/encyclopedie/familiers",
    "/fr/mmorpg/encyclopedie/montures",
    "/fr/mmorpg/encyclopedie/consommables",
    "/fr/mmorpg/encyclopedie/ressources",
    "/fr/mmorpg/encyclopedie/objets-d-apparat",
    "/fr/mmorpg/encyclopedie/havres-sacs",
    "/fr/mmorpg/encyclopedie/harnachements",
    "/fr/mmorpg/encyclopedie/compagnons",
]

dofscraper = DofScraper("https://www.dofus.com")
data = dofscraper.scrape(urls, index=2)

with open("result.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
