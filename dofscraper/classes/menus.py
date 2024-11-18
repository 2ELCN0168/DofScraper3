import questionary
from classes.colors import Colors
from classes.downloader import ImageDownloader
from classes.webscraper import DofScraper


class Menu:
    def __init__(self, title, options):
        self.title = title
        self.options = options

    def display(self):
        answer = questionary.select(self.title, choices=self.options).ask()
        return answer


class Application:
    def __init__(self):
        self.parameters()
        self._main_menu = Menu(
            "Bienvenue dans DofScraper",
            ["Scanner les pages", "Télécharger les images", "Quitter"],
        )
        self._scan_menu = Menu(
            "Menu du Scraper",
            [
                "Tout scraper",
                "Scraper les armes",
                "Scraper les équipements",
                "Scraper le bestiaire",
                "Scraper les familiers",
                "Scraper les montures",
                "Scraper les consommables",
                "Scraper les ressources",
                "Scraper les objets d'apparat",
                "Scraper les havres-sacs",
                "Scraper les harnachements",
                "Scraper les compagnons",
                "Retour",
            ],
        )
        self._download_menu = Menu(
            "Menu de téléchargement",
            [
                "Tout télécharger",
                "Télécharger les armes",
                "Télécharger les équipements",
                "Télécharger le bestiaire",
                "Télécharger les familiers",
                "Télécharger les montures",
                "Télécharger les consommables",
                "Télécharger les ressources",
                "Télécharger les objets d'apparat",
                "Télécharger les havres-sacs",
                "Télécharger les harnachements",
                "Télécharger les compagnons",
                "Retour",
            ],
        )

    def main_menu(self):
        while True:
            choice = self._main_menu.display()
            if choice == "Scanner les pages":
                self.scan_menu()
            elif choice == "Télécharger les images":
                self.download_menu()
            elif choice == "Quitter":
                self.exit()
                break

    def scan_menu(self):
        dofscraper = DofScraper("https://www.dofus.com")
        while True:
            choice = self._scan_menu.display()
            if choice == "Tout scraper":
                dofscraper.scrape(self.urls, self.json_file, index=None)
            elif choice == "Scraper les armes":
                dofscraper.scrape(self.urls, self.json_file, index=0)
            elif choice == "Scraper les équipements":
                dofscraper.scrape(self.urls, self.json_file, index=1)
            elif choice == "Scraper le bestiaire":
                dofscraper.scrape(self.urls, self.json_file, index=2)
            elif choice == "Scraper les familiers":
                dofscraper.scrape(self.urls, self.json_file, index=3)
            elif choice == "Scraper les montures":
                dofscraper.scrape(self.urls, self.json_file, index=4)
            elif choice == "Scraper les consommables":
                dofscraper.scrape(self.urls, self.json_file, index=5)
            elif choice == "Scraper les ressources":
                dofscraper.scrape(self.urls, self.json_file, index=6)
            elif choice == "Scraper les objets d'apparat":
                dofscraper.scrape(self.urls, self.json_file, index=7)
            elif choice == "Scraper les havres-sacs":
                dofscraper.scrape(self.urls, self.json_file, index=8)
            elif choice == "Scraper les harnachements":
                dofscraper.scrape(self.urls, self.json_file, index=9)
            elif choice == "Scraper les compagnons":
                dofscraper.scrape(self.urls, self.json_file, index=10)
            elif choice == "Retour":
                break

    def download_menu(self):
        downloader = ImageDownloader(self.json_file, self.base_folder)
        while True:
            choice = self._download_menu.display()
            if choice == "Tout télécharger":
                selected_category = None
                downloader.process_json(selected_category)
            elif choice == "Télécharger les armes":
                selected_category = "Armes"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les équipements":
                selected_category = "Équipements"
                downloader.process_json(selected_category)
            elif choice == "Télécharger le bestiaire":
                selected_category = "Bestiaire"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les familiers":
                selected_category = "Familiers"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les montures":
                selected_category = "Montures"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les consommables":
                selected_category = "Consommables"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les ressources":
                selected_category = "Ressources"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les objets d'apparat":
                selected_category = "Objets d'apparat"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les havres-sacs":
                selected_category = "Havres-Sacs"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les harnachements":
                selected_category = "Harnachements"
                downloader.process_json(selected_category)
            elif choice == "Télécharger les compagnons":
                selected_category = "Compagnons"
                downloader.process_json(selected_category)
            elif choice == "Retour":
                break

    def exit(self):
        print(
            f"[{Colors.MAGENTA}@{Colors.RESET}] - À bientôt dans {Colors.YELLOW}DofScraper !{Colors.RESET}"
        )

    def parameters(self):

        self.urls = [
            "/fr/mmorpg/encyclopedie/armes",  # 0
            "/fr/mmorpg/encyclopedie/equipements",  # 1
            "/fr/mmorpg/encyclopedie/monstres",  # 2
            "/fr/mmorpg/encyclopedie/familiers",  # 3
            "/fr/mmorpg/encyclopedie/montures",  # 4
            "/fr/mmorpg/encyclopedie/consommables",  # 5
            "/fr/mmorpg/encyclopedie/ressources",  # 6
            "/fr/mmorpg/encyclopedie/objets-d-apparat",  # 7
            "/fr/mmorpg/encyclopedie/havres-sacs",  # 8
            "/fr/mmorpg/encyclopedie/harnachements",  # 9
            "/fr/mmorpg/encyclopedie/compagnons",  # 10
        ]

        self.json_file = "encyclopedie.json"
        self.base_folder = "encyclopedie"
