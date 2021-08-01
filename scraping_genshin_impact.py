import requests
from bs4 import BeautifulSoup
from GI_code import GenshinCode
from GI_reward import GenshinReward
import data_management


class GenshinImpact:
    codes = None
    banners = None
    codes_active_bgcolor = "#9F9"
    url_codes = "https://genshin-impact.fandom.com/wiki/Promotional_Codes"

    def __init__(self):
        '''Cuando se llama al constructor de la clase, lo primero que se fetchea es la copia local de los datos'''
        self.load_saved_data()

    def load_saved_data(self):

        self.codes = data_management.json_to_genshin_codes("./Data/", "GI_codes_data")
        # Si no existen datos se crea el diccionario con la entrada vacía
        if not self.codes:
            self.codes["codes"] = []

        self.banners = data_management.deserialization_json("./Data/", "GI_banners_data")
        # Si no existen datos se crea el diccionario con la entrada vacía
        if not self.banners:
            self.banners["banners"] = []

    def save_data(self):
        data_management.genshin_codes_to_json("./Data/", "GI_codes_data", self.codes)
        data_management.serialization_json("./Data/", "GI_banners_data", self.banners)

    def scrap_codes(self):
        page = requests.get(self.url_codes)

        soup = BeautifulSoup(page.content, "html.parser")

        codes_lines = []

        for line in soup.find('table').find_all('tr'):

            header = line.find('th')
            if header:
                continue

            genshin_code_data = GenshinCode()

            columns = line.find_all('td')

            # Parte dedicada a extraer los códigos promocionales
            code_column = columns[0].code
            external_link = line.find(class_="external text")
            if code_column:
                code_text = code_column.text.split("[")[0]

                if external_link:
                    genshin_code_data.external_link = external_link["href"]
                else:
                    genshin_code_data.external_link = None

                genshin_code_data.promotional_code = code_text.strip()

            else:
                genshin_code_data.promotional_code = "Error getting the code"
                genshin_code_data.external_link = "No available link"

            # Parte dedicada a extraer los servidores en los que se aplican los códigos promocionales
            genshin_code_data.server = columns[1].text.strip()

            # Parte dedicada a extraer las recompensas
            rewards_column = columns[2].get_text().split()
            rewards_list = []

            item_name = []

            for element in rewards_column:

                if "×" not in element:
                    item_name.append(element)
                else:
                    new_item = GenshinReward(" ".join(item_name), element.replace("×", "").replace(",", ""))
                    # item = {"item_name": " ".join(item_name), "quantity": element.replace("×", "").replace(",", "")}
                    rewards_list.append(new_item)
                    item_name = []

            genshin_code_data.rewards = rewards_list

            # Parte dedicada a extraer si el código es valido o no
            if f"background-color:{self.codes_active_bgcolor}" in columns[3].attrs['style']:
                genshin_code_data.status = "Active"
            else:
                genshin_code_data.status = "Expired"

            # Parte dedicada a extraer la duración
            duration_text = columns[3].get_text(separator="¿?)(").strip().split("¿?)(")
            genshin_code_data.start = duration_text[0]

            if len(duration_text) > 1:
                genshin_code_data.end = duration_text[1]
            else:
                genshin_code_data.end = None

            codes_lines.append(genshin_code_data)

        # El diccionario con todos los objetos Code, mapeando los atributos que serán
        # parseados en el JSON
        temp_dict = {"codes": codes_lines}
        return temp_dict

    def check_new_codes(self):

        new_scraped_codes = self.scrap_codes()

        new_codes = []

        for code_data in new_scraped_codes["codes"]:
            if code_data.status == "Active" and code_data not in self.codes["codes"]:
                new_codes.append(code_data)

        if new_codes or new_scraped_codes != self.codes:
            self.codes["codes"] = new_scraped_codes["codes"]
            self.save_data()

        return new_codes

    def get_active_codes(self):

        active_codes = []

        for code_data in self.codes["codes"]:
            if code_data.status == "Active":
                active_codes.append(code_data)

        if active_codes:
            return active_codes
        else:
            return None
