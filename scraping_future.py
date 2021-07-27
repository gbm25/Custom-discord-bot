'''Este script es un previo para poder remplazar la lógica de la clase 
Genshing Impact, y así mapear atributos del JSON que recibe el BOT en objetos personalizados'''

import requests
from bs4 import BeautifulSoup
from code import GenshingCode

page = requests.get("https://genshin-impact.fandom.com/wiki/Promotional_Codes")

soup = BeautifulSoup(page.content, "html.parser")

codes_lines = []

for line in soup.find('table').find_all('tr'):

    header = line.find('th')
    if header:
        continue

    code_entry = {}

    code_entry_obj = GenshingCode()

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
            code_entry_obj.external_link = external_link["href"]

        code_entry_obj.promotional_code = code_text

    else:
        code_entry_obj.promotional_code = "Error getting the code"
        code_entry_obj.external_link = "No availiable link"


    # Parte dedicada a extraer los servidores en los que se aplican los códigos promocionales
    code_entry_obj.server = columns[1].text.strip()

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

    code_entry_obj.rewards = rewards_list

    # Parte dedicada a extraer si el código es valido o no
    if f"background-color:{'#9F9'}" in columns[3].attrs['style']:
        code_entry_obj.status = "Active"
    else:
        code_entry_obj.status = "Expired"

    # Parte dedicada a extraer la duración
    duration_text = columns[3].get_text(separator="¿?)(").strip().split("¿?)(")
    code_entry_obj.start = duration_text[0]

    if len(duration_text) > 1:
        code_entry_obj.end = duration_text[1]
    else:
        code_entry_obj.end = ""

    codes_lines.append(code_entry_obj)

# El diccionario con todos los objetos Code, mapeando los atributos que serán 
# parseados en el JSON
temp_dict = {"codes": codes_lines}

# Resultado
for idx, code in enumerate(temp_dict.get("codes")):
    print('\n******************')
    print(f'RESULTADO núm {idx}')
    print(code.promotional_code)
    print(code.external_link)
    print(code.server)
    print(code.rewards)
    print(code.status)
    print(code.start)
    print(code.end)