import requests
from bs4 import BeautifulSoup

class GenshinImpact:

    def __init__(self):
        self.url_codes = "https://genshin-impact.fandom.com/wiki/Promotional_Codes"
        self.codes_active_bgcolor = "#9F9"
        self.data = {'banners': [{'name': 'Leaves in the Wind', 'type': 'Character Event Wish', 'urls': [
            {'wiki': 'https://genshin-impact.fandom.com/wiki/Leaves_in_the_Wind/2021-06-29',
             'oficial': 'https://genshin.mihoyo.com/en/news/detail/13657'}], 'status': 'Active', 'start': '1624971600',
                                  'end': '1626789599'}, {'name': 'Epitome Invocation', 'type': 'Weapon Event Wish',
                                                         'urls': [{
                                                             'wiki': 'https://genshin-impact.fandom.com/wiki/Leaves_in_the_Wind/2021-06-29',
                                                             'oficial': 'https://genshin.mihoyo.com/en/news/detail/13657'}],
                                                         'status': 'Upcoming', 'start': '1626836400',
                                                         'end': '1628603999'}]}

    def get_codes(self):
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
            item = {}
            item_name = []

            for element in rewards_column:
                if not "×" in element:
                    item_name.append(element)
                else:
                    item["item_name"] = " ".join(item_name)
                    item["quantity"] = element.replace("×", "").replace(",", "")
                    rewards_list.append(item)

            code_entry["rewards"] = rewards_list

            # Parte dedicada a extraer si el código es valido o no

            status = ""

            if (f"background-color:{self.codes_active_bgcolor}" in columns[3].attrs['style']):
                status = "Active"
            else:
                status = "Expired"

            code_entry["status"] = status
            # Parte dedicada a extraer la duración
            duration_text = columns[3].get_text(separator="¿?)(").strip().split("¿?)(")

            code_entry["start"] = duration_text[0]
            code_entry["end"] = duration_text[1]

            codes_lines.append(code_entry)

        self.data["codes"] = codes_lines

