import requests
from bs4 import BeautifulSoup

gi_codes_url = "https://genshin-impact.fandom.com/wiki/Promotional_Codes"

page = requests.get(gi_codes_url)

soup = BeautifulSoup(page.content, "html.parser")

active_bgcolor = "#9F9"
active_font_color = "#3a3a3a"
code_table = soup.findAll("table", class_="wikitable sortable tdl3 tdl4")

for element in code_table:
    table_lines = element.find_all('tr')

external_urls = []
counter = 0
for line in table_lines:
    header = line.find('th')
    if header:
        continue

    columns = line.find_all('td')

    # Parte dedicada a extraer los códigos promocionales
    code_column = columns[0].code
    external_link = line.find(class_="external text")
    if code_column:
        code_text = code_column.text.split("[")[0]
        if external_link:
            external_urls.append(external_link["href"])
            code_text += f'\r\n+ info click en enlace {len(external_urls)}'
    else:
        print("error al recuperar el texto")

    # Parte dedicada a extraer los códigos promocionales
    server_text = columns[1].text.strip()

    # Parte dedicada a extraer las recompensas
    rewards_column = columns[2].get_text().split()
    rewards_list = {}
    item_name = []

    for element in rewards_column:
        if not "×" in element:
            item_name.append(element)
        else:
            rewards_list[" ".join(item_name)] = element
            item_name = []

    # Parte dedicada a extraer la duración
    duration_text = columns[3].get_text(separator="¿?)(").split("¿?)(")

    print(f'Codigo Nº{counter}: {code_text}\r\n On Server:{server_text}\r\n Rewards: {rewards_list} \r\n Duration: {duration_text}')

