import json
import os

import requests
from classes.colors import Colors
from unidecode import unidecode


class ImageDownloader:
    def __init__(self, json_file, base_folder):
        self.json_file = json_file
        self.base_folder = base_folder

    def create_folder(self, path):
        """Create folder if not existing"""
        if not os.path.exists(path):
            os.makedirs(path)

    def sanitize_name(self, name):
        """Convert to [:alnum:] names"""
        return unidecode(name).lower()

    def download_image(self, url, save_path):
        """Download the image and save it to the path"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as out_file:
                for chunk in response.iter_content(1024):
                    out_file.write(chunk)
        except requests.exceptions.RequestException as e:
            print(f"Erreur pendant le téléchargement : {e}")

    def process_json(self, selected_category=None):
        """Process the JSON file and download file"""
        with open(self.json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        category_to_process = [selected_category] if selected_category else data.keys()

        for category in category_to_process:
            if category not in data:
                print(
                    f"[{Colors.RED}!{Colors.RESET}] - {Colors.RED}Erreur, la catégorie n'existe pas, l'avez-vous scannée ?"
                )
                continue
            sanitized_category = self.sanitize_name(category)
            category_data = data[category]

            if isinstance(category_data, dict):
                for item_type, items in category_data.items():
                    sanitized_type = self.sanitize_name(item_type)
                    type_folder = os.path.join(
                        self.base_folder, sanitized_category, sanitized_type
                    )
                    self.create_folder(type_folder)

                    for item in items:
                        self.process_item(item, type_folder)
            elif isinstance(category_data, list):
                type_folder = os.path.join(self.base_folder, sanitized_category)
                self.create_folder(type_folder)

                for item in category_data:
                    self.process_item(item, type_folder)

    def process_item(self, item, folder):
        """Process and download a single item"""
        item_slug = os.path.basename(item["link"])
        if item["level"]:
            item_name = f"{item['level']}_{item_slug}"
        else:
            item_name = item_slug

        image_url = item["picture"]
        if not image_url:
            image_url = "https://static.ankama.com/dofus/www/game/items/200/0.png"

        image_extension = os.path.splitext(image_url)[1]
        image_path = os.path.join(folder, f"{item_name}{image_extension}")

        print(
            f"{Colors.CYAN}[{Colors.YELLOW}+{Colors.CYAN}] - {Colors.GREEN}Téléchargement de l'image pour {Colors.YELLOW}{item['name']}{Colors.RESET}"
        )
        self.download_image(image_url, image_path)
