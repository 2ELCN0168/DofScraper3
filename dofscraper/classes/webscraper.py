import json
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from classes.colors import Colors
from tqdm import tqdm


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
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(
                    f"\n[{Colors.RED}>{Colors.RESET}] - {Colors.MAGENTA}Blocage temporaire du serveur, reprise dans 5 minutes.{Colors.RESET}\n"
                )
                for _ in tqdm(range(300), desc="Waiting", unit="s"):
                    time.sleep(1)
                return self.fetch_page(path)
        except requests.exceptions.RequestException as e:
            print(
                f"\n[{Colors.RED}!{Colors.RESET}] - {Colors.RED}Error fetching the page : {Colors.YELLOW}{e}{Colors.RESET}"
            )
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
            if encyclo_illus:
                img_src = encyclo_illus.get("src")
                if not img_src:
                    img_src = encyclo_illus.get("data-src")
                return (
                    img_src
                    if img_src
                    else "https://static.ankama.com/dofus/www/game/items/200/0.png"
                )
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

    def determine_master_category(self, item_url):
        """Returns master category based on the URL"""
        if "/armes" in item_url:
            return "Armes"
        elif "/equipements" in item_url:
            return "Équipements"
        elif "/monstres" in item_url:
            return "Bestiaire"
        elif "/familiers" in item_url:
            return "Familiers"
        elif "/montures" in item_url:
            return "Montures"
        elif "/consommables" in item_url:
            return "Consommables"
        elif "/ressources" in item_url:
            return "Ressources"
        elif "/objets-d-apparat" in item_url:
            return "Objets d'apparat"
        elif "/havres-sacs" in item_url:
            return "Havres-Sacs"
        elif "/harnachements" in item_url:
            return "Harnachements"
        elif "/compagnons" in item_url:
            return "Compagnons"
        else:
            return "Catégorie manquante"

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
        return item_data

    def save_item(self, output_file, category, items):
        """Save each item in the JSON output file"""
        try:
            with open(output_file, "r", encoding="utf-8") as f:
                content = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            content = {}

        if category not in content:
            content[category] = {}

        for item in items:
            item_type = item.get("type")

            if category == "Bestiaire":
                family = item.get("family", "Inconnu")
                if family not in content[category]:
                    content[category][family] = []
                content[category][family].append(item)
            elif item_type:
                if item_type not in content[category]:
                    content[category][item_type] = []
                content[category][item_type].append(item)
            else:
                # Pour les items sans type, ajoutez-les directement sous la catégorie
                if not isinstance(content[category], list):
                    content[category] = []  # Assurez-vous que ce soit une liste
                content[category].append(item)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=2)

    def process_page(
        self, base_url, output_file, category, type_name=None, filter_param=None
    ):
        """Generic method to process pages"""
        page = 1

        while True:
            items = []
            url = f"{base_url}?page={page}"
            if filter_param:
                url += f"&{filter_param}"
            print(
                f"[{Colors.BLUE}:{Colors.RESET}] - {Colors.YELLOW}Collecte de la page : {Colors.CYAN}{url}{Colors.RESET}"
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
                    if type_name:
                        item_info["type"] = type_name
                    items.append(item_info)

                    print(
                        f"[ Lien : {Colors.BLUE}{item_info['link']}{Colors.RESET} ][ "
                        f"Nom : {Colors.YELLOW}{item_info['name']}{Colors.RESET} ][ "
                        f"Type : {Colors.MAGENTA}{item_info['type']}{Colors.RESET} ][ "
                        f"Niveau : {Colors.RED}{item_info['level']}{Colors.RESET} ][ "
                        f"Famille : {Colors.CYAN}{item_info['family']}{Colors.RESET} ]"
                    )

            self.save_item(output_file, category, items)
            page += 1
        return items

    def process_items(self, _url, output_file):
        category = self.determine_master_category(_url)

        if "/montures" in _url:
            mount_filters = {
                "Dragodinde": "model_family_id%5B%5D=1",
                "Muldo": "model_family_id%5B%5D=5",
            }

            items = []
            for mount_type, filter_param in mount_filters.items():
                items.extend(
                    self.process_page(
                        _url, output_file, category, mount_type, filter_param
                    )
                )
        elif "/monstres" in _url:
            items = self.process_page(_url, output_file, "Bestiaire")
        else:
            items = self.process_page(_url, output_file, category)
        return items

    def scrape(self, urls, output_file, index=None):

        all_data = []

        if index is not None:
            urls = [urls[index]]

        try:
            for url in urls:
                items = self.process_items(url, output_file)
                all_data.extend(items)
        except (KeyboardInterrupt, EOFError):
            print(
                f"\n[{Colors.RED}!{Colors.RESET}] - Scraping interrompu. {Colors.GREEN}Sauvegarde des données avant arrêt...{Colors.RESET}"
            )
            sys.exit(0)
        except Exception as e:
            print(
                f"[{Colors.RED}!{Colors.RESET}] - {Colors.RED}Une erreur a eu lieu : {e}. {Colors.GREEN}Sauvegarde des données avant arrêt...{Colors.RESET}"
            )
            raise
        finally:
            print(
                f"{Colors.CYAN}[{Colors.YELLOW}+{Colors.CYAN}] - {Colors.GREEN}Scraping terminé. Sauvegarde dans le fichier JSON.{Colors.RESET}"
            )
        return all_data
