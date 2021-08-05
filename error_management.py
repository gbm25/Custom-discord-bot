import os
from datetime import datetime


def create_log(relative_path, message):

    now = datetime.today()
    try:
        if not os.path.exists(f'{relative_path}'):
            os.mkdir(f'{relative_path}')
        with open(f'{relative_path}{now.date()}.txt', 'a+') as file:

            file.write(f'[{now.strftime("%d/%m/%Y, %H:%M:%S")}]: {message}')

        file.close()

    except Exception as e:
        print(f"Error guardando logs\r\n Error : {e}")
