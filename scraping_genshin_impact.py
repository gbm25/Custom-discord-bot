import requests
from bs4 import BeautifulSoup
import data_management


class GenshinImpact:
    codes = None
    banners = None
    codes_active_bgcolor = "#9F9"
    url_codes = "https://genshin-impact.fandom.com/wiki/Promotional_Codes"

    def __init__(self):
        self.load_saved_data()

    def load_saved_data(self):

        self.codes = data_management.deserialization_json("./Data/", "GI_codes_data")
        if not self.codes:
            self.codes["codes"] = []
        self.banners = data_management.deserialization_json("./Data/", "GI_banners_data")
        if not self.banners:
            self.banners["banners"] = []

    def save_data(self):
        data_management.serialization_json("./Data/", "GI_codes_data", self.codes)
        data_management.serialization_json("./Data/", "GI_banners_data", self.banners)

    def scrap_codes(self):
        page = requests.get(self.url_codes)

        soup = BeautifulSoup(page.content, "html.parser")
        code_table = soup.findAll("table", class_="wikitable sortable tdl3 tdl4")

        for element in code_table:
            table_lines = element.find_all('tr')

        codes_lines = []

        for line in table_lines:

            header = line.find('th')
            if header:
                continue
            code_entry = {}

            columns = line.find_all('td')

            # Parte dedicada a extraer los códigos promocionales
            code_column = columns[0].code
            external_link = line.find(class_="external text")
            if code_column:
                code_text = code_column.text.split("[")[0]
                code_entry["code"] = code_text
                code_entry["external_link"] = None
                if external_link:
                    code_text += f'\r\n+ info click en enlace {external_link["href"]}'
                    code_entry["external_link"] = external_link["href"]
            else:
                code_entry["code"] = "Error getting the code"
                code_entry["external_link"] = "Error getting the code"

            # Parte dedicada a extraer los servidores en los que se aplican los códigos promocionales
            server_text = columns[1].text.strip()
            code_entry["server"] = server_text

            # Parte dedicada a extraer las recompensas
            rewards_column = columns[2].get_text().split()
            rewards_list = []

            item_name = []

            for element in rewards_column:
                if "×" not in element:
                    item_name.append(element)
                else:
                    item = {"item_name": " ".join(item_name), "quantity": element.replace("×", "").replace(",", "")}

                    rewards_list.append(item)
                    item_name = []

            code_entry["rewards"] = rewards_list

            # Parte dedicada a extraer si el código es valido o no

            if f"background-color:{self.codes_active_bgcolor}" in columns[3].attrs['style']:
                status = "Active"
            else:
                status = "Expired"

            code_entry["status"] = status
            # Parte dedicada a extraer la duración
            duration_text = columns[3].get_text(separator="¿?)(").strip().split("¿?)(")

            code_entry["start"] = duration_text[0]
            code_entry["end"] = duration_text[1]

            codes_lines.append(code_entry)
        temp_dict = {"codes": codes_lines}
        return temp_dict

    def check_new_codes(self):

        new_scraped_codes = self.scrap_codes()

        new_codes = []

        for code_data in new_scraped_codes["codes"]:
            if code_data["status"] == "Active" and code_data not in self.codes["codes"]:
                new_codes.append(code_data)

        if new_codes or new_scraped_codes["codes"] != self.codes["codes"]:
            self.codes["codes"] = new_scraped_codes["codes"]
            self.save_data()
        print(self.codes)
        return new_codes

    def get_active_codes(self):

        active_codes = []

        for code_data in self.codes["codes"]:
            if code_data["status"] == "Active":
                active_codes.append(code_data)

        if active_codes:
            return active_codes
        else:
            return None
