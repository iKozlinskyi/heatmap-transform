from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from src import heatmap_transform
import numpy as np
import re
from datetime import datetime
import textwrap

hostName = "91.219.60.147"
serverPort = 8080


def exp_data_to_float_arr(raw_data: str):
    res = np.array([x for x in raw_data.split(",")]).reshape((8, 8))
    return np.float64(res)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def save_raw_data(date, raw_data):
    raw_data = "\n".join(textwrap.wrap(raw_data, 48))
    with open("./data/raw/data.txt", 'a') as f:
        f.write(str(date) + "\n")
        f.write(raw_data + "\n")

def process_data(raw_data: str):
    date = datetime.now()
    filename = get_valid_filename(date)
    save_raw_data(date, raw_data)
    data_arr = exp_data_to_float_arr(raw_data)
    heatmap_transform.save_heatmap(data_arr, filename)


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        query = urlparse(self.path).query
        query_components = parse_qs(query)
        data = query_components.get('s')
        if data:
            process_data(data[0])


if __name__ == "__main__":
    Path("./data/processed").mkdir(parents=True, exist_ok=True)
    Path("./data/raw").mkdir(parents=True, exist_ok=True)
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
