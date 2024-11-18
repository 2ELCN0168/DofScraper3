# from classes.colors import Colors
# from classes.downloader import ImageDownloader
from classes.menus import Application

# from classes.webscraper import DofScraper
#
# urls = [
#     "/fr/mmorpg/encyclopedie/armes",  # 0
#     "/fr/mmorpg/encyclopedie/equipements",  # 1
#     "/fr/mmorpg/encyclopedie/monstres",  # 2
#     "/fr/mmorpg/encyclopedie/familiers",  # 3
#     "/fr/mmorpg/encyclopedie/montures",  # 4
#     "/fr/mmorpg/encyclopedie/consommables",  # 5
#     "/fr/mmorpg/encyclopedie/ressources",  # 6
#     "/fr/mmorpg/encyclopedie/objets-d-apparat",  # 7
#     "/fr/mmorpg/encyclopedie/havres-sacs",  # 8
#     "/fr/mmorpg/encyclopedie/harnachements",  # 9
#     "/fr/mmorpg/encyclopedie/compagnons",  # 10
# ]
#
# dofscraper = DofScraper("https://www.dofus.com")
# data = dofscraper.scrape(urls, "result.json", index=1)
# json_file = "result.json"
# base_folder = "encyclopedie"

# downloader = ImageDownloader(json_file, base_folder)
# downloader.process_json()


def main():
    app = Application()
    app.main_menu()


if __name__ == "__main__":
    main()
