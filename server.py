from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from src import heatmap_transform
import numpy as np
import re
from datetime import datetime
import textwrap

# Настройки для адреса/порта, по которому слушать запросы
hostName = "91.219.60.147"
serverPort = 8080


# Принимает сырые данные - строку из разделенных запятой значений
# Возвращает матрицу значений (8 на 8)
def exp_data_to_float_arr(raw_data: str):
    """
    Сначаа сырые данные разбиваем по запятой (raw_data.split(","))
    получаем массив (одномерный) строк
    Запихиваем это в np.array() - чтобы получить новые методы
    для работы с массивами
    
    Затем перегруппировываем одномерный массив длинной в 64 элемента в 
    двумерный массив 8 на 8 (8 массивов по 8 элементов) - .reshape((8, 8))
    
    Затем превращаем строковые значения в массиве в числа - np.float64(string_matrix)
    """
    string_matrix = np.array(raw_data.split(",")).reshape((8, 8))
    return np.float64(string_matrix)


def get_valid_filename(s):
    """
    Для строки s убираем невалидные символы для имени файла
    """
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def save_raw_data(date, raw_data):
    """
    получаем текущее время и сырые данные
    Разбиваем сырые данные на массивы (длинной 48 символов) - textwrap.wrap(raw_data, 48)
    Полученный массив строк соединяем символом переноса строки - "\n".join(...)
    """
    raw_data = "\n".join(textwrap.wrap(raw_data, 48))
    with open("./data/raw/data.txt", 'a') as f:
        #  Пишем в файл сначала дату, потом данные. Добавляем переносы строк
        f.write(str(date) + "\n")
        f.write(raw_data + "\n")


def process_data(raw_data: str):
    """
    Получаем сырые данные
    """
    # Получаем текущую дату
    date = datetime.now()
    # Удаляем из даты невалидніе символы
    filename = get_valid_filename(date)
    # Сохраняем данные
    save_raw_data(date, raw_data)
    # Превращяем сырые данные в матрицу чисел
    data_arr = exp_data_to_float_arr(raw_data)
    # Обрабатываем значения для получения картинки
    heatmap_transform.save_heatmap(data_arr, filename)


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Код выполнится при получении GET запроса
        # устанавливаем ответ
        self.send_response(200)
        self.end_headers()

        # парсим запрос - достаем сырые данные
        query = urlparse(self.path).query
        query_components = parse_qs(query)
        data = query_components.get('s')
        # Если данные есть - обрабатываем
        if data:
            process_data(data[0])


# Этот код выполнится при запуске скрипта с консоли
# считай это "точкой входа"
# типа int main() {} в языкaх C/C++
if __name__ == "__main__":
    # Создаем папки для сохранения картинок и данных
    Path("./data/processed").mkdir(parents=True, exist_ok=True)
    Path("./data/raw").mkdir(parents=True, exist_ok=True)
    # Создаем экземпляр класса веб сервера (класс написали выше)
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Запускаем сервер
        webServer.serve_forever()
        # Если нажато Ctrl+C (сингал KeyboardInterrupt) в консоли, пока сервер слушает команды
        # он остановится
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
