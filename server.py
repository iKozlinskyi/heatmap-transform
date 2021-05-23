from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from src import heatmap_transform
import numpy as np
import re
from datetime import datetime

hostName = "localhost"
serverPort = 8080


def exp_data_to_float_arr(exp_data_arr):
    res = [x[:-1].split(",") for x in exp_data_arr]
    return np.float64(res)

def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def save_raw_data(raw_data, filename):
    with open("./data/raw/%s.txt" % filename, 'w') as f:
        f.write(raw_data)

def process_data(raw_data: str):
    lines = np.array(raw_data.strip().split("\n"))
    group_by_experiment = lines.reshape(int(len(lines) / 9), 9)
    save_raw_data(raw_data, get_valid_filename(datetime.now()))
    for experiment in group_by_experiment:
        exp_timestamp = experiment[0]
        exp_data = exp_data_to_float_arr(experiment[1:])
        filename = get_valid_filename(exp_timestamp)
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
