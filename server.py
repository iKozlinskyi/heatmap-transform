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


def exp_data_to_float_arr(exp_data_arr):
    res = [x[:-1].split(",") for x in exp_data_arr]
    return np.float64(res)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def save_raw_data(date, raw_data, filename):
    with open("./data/raw/data.txt", 'a') as f:
        f.write(str(date) + "\n")
        f.write(raw_data + "\n")

def process_data(raw_data: str):
    raw_data = "\n".join(textwrap.wrap(raw_data, 48))

    lines = np.array(raw_data.strip().split("\n"))
    group_by_experiment = lines.reshape(int(len(lines) / 8), 8)
    date = datetime.now()
    filename = get_valid_filename(date)
    save_raw_data(date, raw_data, filename)
    for experiment in group_by_experiment:
        exp_data = exp_data_to_float_arr(experiment)
        heatmap_transform.save_heatmap(exp_data, filename)


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
