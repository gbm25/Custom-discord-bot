import requests
from bs4 import BeautifulSoup
import re
from GI_code import GenshinCode
from GI_reward import GenshinReward
from GI_banner import GenshinBanner
import data_management


class GenshinImpact:
    codes = None
    banners = None

    codes_active_bgcolor_hex = "#9F9"
    codes_active_bg_color_rgb = "153,255,153"
    url_codes = "https://genshin-impact.fandom.com/wiki/Promotional_Codes"

    base_fandom_url = "https://genshin-impact.fandom.com"
    base_banners_url = "https://genshin-impact.fandom.com/wiki/Wishes/List"

    def __init__(self):
        """Cuando se llama al constructor de la clase, lo primero que se fetchea es la copia local de los datos"""

        self.load_saved_data()

    def load_saved_data(self):
        """Carga los datos almacenados de forma local"""

        self.codes = data_management.json_to_genshin_codes("./Data/", "GI_codes_data")
        # Si no existen datos se crea el diccionario con la entrada vacía
        if not self.codes:
            self.codes["codes"] = []

        self.banners = data_management.json_to_genshin_banners("./Data/", "GI_banners_data")
        # Si no existen datos se crea el diccionario con la entrada vacía
        if not self.banners:
            self.banners["banners"] = []

    def save_data(self):
        """Guarda los datos en archivos locales"""

        data_management.genshin_codes_to_json("./Data/", "GI_codes_data", self.codes)
        data_management.genshin_banners_to_json("./Data/", "GI_banners_data", self.banners)

    def scrap_codes(self):
        """Realiza scraping en la wiki de Genshin impact para recolectar datos sobre los códigos promocionales"""

        page = requests.get(self.url_codes)

        soup = BeautifulSoup(page.content, "html.parser")

        codes_lines = []

        # Iteramos sobre todas las lineas (etiqueta html "tr") de la tabla de códigos
        for line in soup.find('table').find_all('tr'):

            # Comprobamos si la linea es la cabecera, definida por la etiqueta html "th"
            # De ser así pasamos a la siguiente iteración, pues la cabecera no aporta ningún dato relevante
            header = line.find('th')
            if header:
                continue

            # Se crea el objeto de tipo GenshinCode, donde se irán almacenando los datos de la linea
            genshin_code_data = GenshinCode()

            # Se separa la fila en columnas, cada columna es definida por la etiqueta html "td"
            columns = line.find_all('td')

            # PARTE DEDICADA A EXTRAER EL CÓDIGO PROMOCIONAL Y EL ENLACE EXTERNO DE LA PRIMERA COLUMNA

            # Se almacena en una variable el contenido de la etiqueta html "code"
            code_column = columns[0].code

            # Se almacena en una variable el contenido de la primera etiqueta que se encuentre
            # con un atributo "class" igual a "external text"
            # Cabe señalar que solo debería existir una coincidencia en esta columna
            external_link = code_column.find(class_="external text")

            # Si existen datos del código promocional lo extraemos y añadimos al objeto.
            # En caso de existir un enlace un enlace externo para la promoción, también se añade.
            # Esto es así porque no siempre se extrae un código promocional directamente usable en el juego,
            # ocasionalmente se extrae texto, y un enlace al que hay que acceder para obtener el código.
            if code_column:
                code_text = code_column.text.split("[")[0]

                if external_link:
                    genshin_code_data.external_link = external_link["href"]

                genshin_code_data.promotional_code = code_text.strip()

            # En caso de no contener datos se añade mensajes de error en el objeto para esos apartados
            else:
                genshin_code_data.promotional_code = "Error getting the code"
                genshin_code_data.external_link = "No available link"

            # PARTE DEDICADA A EXTRAER EL/LOS SERVIDOR/ES EN LOS QUE EL CÓDIGO ES APLICABLE

            # Se añade al objeto el texto contenido entre las etiquetas html de la segunda columna de la linea.
            # eliminando previamente los espacios al principio y al final
            genshin_code_data.server = columns[1].text.strip()

            # PARTE DEDICADA A EXTRAER LAS RECOMPENSAS

            # Se almacena en una variable las recompensas que se encuentran en la tercera columna de la linea.
            # Se almacenan en formato lista usando split(), pues las recompensas están separadas por salto de linea
            # Tendrá el siguiente formato:
            # [
            # Nombre,
            # Del,
            # Objeto,
            # ×Cantidad,
            # NombreDelObjeto2,
            # ×Cantidad,
            # ]
            rewards_column = columns[2].get_text().split()

            # Se inicializa una variable como array vacío, que ira acumulando las recompensas, siendo objetos
            # GenshinReward
            rewards_list = []

            # Se inicializa una variable como array vacío, que ira acumulando el nombre de la recompensa.
            # Esto se hace por el formato en el que se guardan los datos de las recompensas,
            # por lo que hay que recomponer el nombre si es un nombre compuesto.
            item_name = []

            # Se itera sobre la lista de recompensas
            for element in rewards_column:

                # Si el elemento no contiene el carácter "×" significa que es parte del nombre del objeto,
                # por lo que se añade a la variable definida anteriormente
                if "×" not in element:
                    item_name.append(element)

                # Si el elemento contiene el carácter "×" significa que contiene la cantidad del objeto, Se crea un
                # objeto GenshinReward, compuesto por unir por espacios las palabras almacenadas en la variable para
                # reconstruir el nombre del objeto y la cantidad sin el carácter "×" y quitando la coma.
                # Se añade el objeto a la lista de recompensas.
                # Se resetea el valor de la variable que acumula el nombre del objeto
                else:
                    new_item = GenshinReward(" ".join(item_name), element.replace("×", "").replace(",", ""))

                    rewards_list.append(new_item)
                    item_name = []

            genshin_code_data.rewards = rewards_list

            # PARTE DEDICADA A EXTRAER EL ESTADO DEL CÓDIGO

            # Si el atributo de clase que contiene el color de las lineas activas se encuentra el atributo "style" de
            # alguna etiqueta html de la cuarta columna, el estado es activo y se establece como "Active" en el objeto.
            # De no ser asi, se considerá como expirado y se establece como "Expired" en el objeto.
            if f"background-color:{self.codes_active_bgcolor_hex}" in columns[3].attrs['style'] \
                    or f"background-color:rgb({self.codes_active_bg_color_rgb}" in columns[3].attrs['style']:
                genshin_code_data.status = "Active"
            else:
                genshin_code_data.status = "Expired"

            # PARTE DEDICADA A EXTRAER LA DURACIÓN DEL CÓDIGO
            # WARNING !!! Esta parte necesita más trabajo, es una versión inicial sin pulir !!!

            # Se almacena en formato lista el texto contenido en la cuarta columna de la linea
            # El formato del texto suele ser:
            # "Fecha de comienzo"
            # "Fecha de fin"
            # Este formato no siempre se cumple, pues al ser una tabla actualizada de forma colaborativa,
            # suele ser inconsistente con el formato.
            # Es necesario un análisis más profundo para poder rehacer esta parte.
            duration_text = columns[3].get_text(separator="¿?)(").strip().split("¿?)(")

            # Iteramos sobre las lineas recuperadas
            # Es probable que en ocasiones no contenga la fecha de comienzo y/o fin, e incluso que contenga
            # otros elementos
            for duration_line in duration_text:

                # Comprobamos si en la linea se encuentra el patrón siguiente:
                # Palabra + Espacio + 1 o 2 dígitos + coma + 0 o 1 espacio + 4 dígitos
                if re.search(r"\w+\s\d{1,2},\s?\d{4}", duration_line):
                    # Comprobamos si en la linea se encuentra el patrón:
                    # Discovered + espacio o : 0 o más veces
                    if re.search(r"Discovered(\s|:)*", duration_line):
                        # De encontrarse, se extrae ese patrón y se añade al objeto
                        genshin_code_data.start = re.search(r"\w+\s\d{1,2},\s?\d{4}", duration_line).group(0)
                        # Valid until o Expired + espacio o : 0 o más veces
                    if re.search(r"(Valid until|Expired)(:|\s)*", duration_line):
                        # De encontrarse, se extrae ese patrón y se añade al objeto
                        genshin_code_data.end = re.search(r"\w+\s\d{1,2},\s?\d{4}", duration_line).group(0)

            # # Una vez todos los datos añadidos al objeto GenshinCode, lo añadimos a la variable que los va acumulando.
            codes_lines.append(genshin_code_data)

        # Se crea un diccionario con clave "codes" y con valor todos los objetos GenshinCode.
        temp_dict = {"codes": codes_lines}
        # Se devuelve el diccionario.
        return temp_dict

    def check_new_codes(self):
        """Comprueba si hay cambios en la tabla de códigos promocionales, actualizando los datos del atributo y
        guardándolos en ficheros locales. Devuelve los códigos nuevos con estado activo."""

        # Se llama a la función que realiza scraping de los códigos promocionales y se almacenan los datos que devuelve.
        new_scraped_codes = self.scrap_codes()

        # Se inicializa un array vacío, que almacenará los códigos activos que no estuvieran ya almacenados.
        new_codes = []

        # Iteramos sobre el valor (objetos GenshinCode) de la clave "codes" del diccionario,
        # añadimos a la variable anteriormente inicializada las lineas que no tengamos ya registradas
        # y que tengan estado activo ("Active")
        for code_data in new_scraped_codes["codes"]:
            if code_data.status == "Active" and code_data not in self.codes["codes"]:
                new_codes.append(code_data)

        # Si hay nuevos códigos con estado activo que no teníamos registrados, o la tabla de códigos ha cambiado
        # remplazamos los datos que tenemos por los de la nueva tabla, y guardamos los datos en archivos locales.
        if new_codes or new_scraped_codes != self.codes:
            self.codes["codes"] = new_scraped_codes["codes"]
            self.save_data()

        # Devolvemos un array vacío o con los nuevos códigos con estado activo que no teníamos registrados
        return new_codes

    def get_active_codes(self):
        """Devuelve un array de objetos GenshinCode que contiene los códigos que aún están activos"""

        # Se inicializa un array vacío, que almacenará los códigos activos que tenemos registrados.
        active_codes = []

        # Iteramos sobre el valor (objetos GenshinCode) de la clave "codes" de los códigos que tenemos registrados.
        # Añadimos a la variable anteriormente inicializada las lineas con códigos activos (que se pueden usar).
        for code_data in self.codes["codes"]:
            if code_data.status == "Active":
                active_codes.append(code_data)

        # Devolvemos un array vacío o los códigos con estado activo.
        return active_codes

    def refresh_codes(self, force=False):
        """Comprueba si hay nuevos elementos en la tabla, si los hay, guarda los datos en local.
        Se puede forzar y sobreescribir los datos"""

        # Se llama a la función que realiza scraping de los códigos promocionales y se almacenan los datos que devuelve.
        new_scraped_codes = self.scrap_codes()

        # Si hay nuevos códigos o se fuerza a sobreescribir los datos, remplazamos los datos que tenemos
        # por los de la nueva tabla, y guardamos los datos en archivos locales.
        if new_scraped_codes != self.codes or force:
            self.codes = new_scraped_codes
            self.save_data()

    @staticmethod
    def extract_banner_info_fandom(url):

        def get_datetime_format(datetime_str: str):
            datetime_format = '%B %d, %Y %I:%M:%S %p'

            if ' UTC' in datetime_str.upper() or ' GMT' in datetime_str.upper():
                datetime_format += ' %Z'
            if '+' in datetime_str or '-' in datetime_str:
                datetime_format += '%z'
            return datetime_format

        def normalize_datetime_offset(datetime_str: str):
            datetime_str = datetime_str.strip()
            offset_time = None
            offset_simbol = None
            if "+" in datetime_str:
                offset_simbol = '+'
                offset_time = datetime_str.split("+")[1]
            elif "-" in datetime_str:
                offset_simbol = '-'
                offset_time = datetime_str.split("-")[1]

            if offset_time:
                if len(offset_time) == 1:
                    return f'{datetime_str.split(offset_simbol)[0]}{offset_simbol}0{offset_time}00'
                else:
                    return f'{datetime_str.split(offset_simbol)[0]}{offset_simbol}{offset_time}00'
            return datetime_str

        fandom_page = requests.get(url)
        source = BeautifulSoup(fandom_page.content, "html.parser")

        banner_data = GenshinBanner()

        banner_data.name = source.find(id="firstHeading").text.strip().split('/')[0]
        banner_data.url_fandom = url

        event_body = source.find("div", {"class": "mw-parser-output"}).findChildren(recursive=False)

        duration = None
        official_url = None
        image = None
        date_format = r'(\w+\s\d{1,2},\s\d{4}\s(?:\d{2}:?)+(?:\w|\s|\+|-)*)'

        for element in event_body:
            if "Duration:" in element.get_text():
                duration = element.get_text().split('\n')
                continue
            if "Official announcement" in element.get_text():
                official_url = element.a.get('href')
            if element.find("a", {"class": "image"}):
                image = element.find("a", {"class": "image"}).get('href')

        if duration:
            matches = re.findall(date_format, duration[0])

            start = normalize_datetime_offset(matches[0])
            start_format = get_datetime_format(matches[0])

            banner_data.set_start_time(start, start_format)

            end = normalize_datetime_offset(matches[1])
            end_format = get_datetime_format(matches[1])

            banner_data.set_end_time(end, end_format)

        banner_data.image = image
        banner_data.url_official = official_url

        return banner_data

    def banners_table_to_dict(self, table, status: str):
        banners = []

        if not table:
            return banners

        banners_columns = table.find_all('td')

        if banners_columns:
            for banner in banners_columns:

                if banner.a:
                    fandom_url = f'https://genshin-impact.fandom.com{banner.a.get("href")}'
                    banner_data = self.extract_banner_info_fandom(fandom_url)
                else:
                    banner_data = GenshinBanner(name=banner.span.text)

                if "Epitome" in banner_data.name:
                    banner_data.wish_type = "Weapon"
                else:
                    banner_data.wish_type = "Character"

                banner_data.status = status

                banners.append(banner_data)

        return banners

    def scrap_banners_table(self, banner_status: str):
        banner_status = banner_status.capitalize()

        if banner_status not in ["Current", "Upcoming"]:
            raise ValueError("WonK ! Current or Upcoming expected")

        request = requests.get(self.base_banners_url)
        source = BeautifulSoup(request.content, "html.parser")

        banners = source.find(id=f'{banner_status}').parent.next_siblings

        for banner_html in banners:

            if not banner_html or banner_html == "\n" or banner_html == " ":
                continue

            else:
                return self.banners_table_to_dict(banner_html, banner_status)

        return []

    def check_new_banners(self):
        """Comprueba si hay cambios en las tablas de banners activos (Current) o por venir (Upcoming), actualizando
        los datos del atributo y guardándolos en ficheros locales. Devuelve un diccionario con claves "currents" y
        "upcoming" que contienen los banners nuevos para cada sección"""

        new_scraped_banners_current = self.scrap_banners_table("current")
        new_scraped_banners_upcoming = self.scrap_banners_table("upcoming")

        new_scraped_banners = {'banners': new_scraped_banners_current + new_scraped_banners_upcoming}

        new_banners_current = []
        new_banners_upcoming = []

        for banner in new_scraped_banners_current:
            if banner not in self.banners['banners']:
                new_banners_current.append(banner)

        for banner in new_scraped_banners_upcoming:
            if banner not in self.banners['banners'] and banner.url_fandom:
                new_banners_upcoming.append(banner)

        if self.banners != new_scraped_banners:
            self.banners = new_scraped_banners
            self.save_data()

        return {"currents": new_banners_current, "upcoming": new_banners_upcoming}

    def get_current_banners(self):
        return [banner for banner in self.banners['banners'] if banner.status == "Current" and banner.url_fandom]

    def get_upcoming_banners(self):
        return [banner for banner in self.banners['banners'] if banner.status == "Upcoming" and banner.url_fandom]
