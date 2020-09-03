from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import threading
import os
import cgi
import json
import logging
import requests
import time

from urllib.parse import urlparse

from pathlib import Path
from RPA.Browser import Browser
from collections import OrderedDict


LOGGER = logging.getLogger(__name__)


class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, headertype="json"):
        self.send_response(200)
        if headertype == "json":
            self.send_header("Content-type", "application/json")
        else:
            self.send_header("Content-type", "text/html")
        self.end_headers()

    def create_form(self, message):
        formhtml = "<form action='formresponsehandling'>"
        for item in message["form"]:
            if item["type"] == "input":
                if item["subtype"] == "text":
                    formhtml += (
                        f"<label for=\"{item['name']}\">{item['label']}</label><br>"
                        f"<input type=\"{item['subtype']}\" name=\"{item['name']}\"><br>"
                    )
                elif item["subtype"] == "radio":
                    if "label" in item:
                        formhtml += f"<p>{item['label']}</p>"
                    for option in item["options"]:
                        checkedvalue = ""
                        if "default" in item and item["default"] == option:
                            checkedvalue = " checked"
                        formhtml += f"""<input type=\"radio\" id=\"{option}\" name=\"{item['id']}\" value="{option}"{checkedvalue}>
                                        <label for=\"{option}\">{option}</label><br>"""
                elif item["subtype"] == "checkbox":
                    if "label" in item:
                        formhtml += f"<p>{item['label']}</p>"
                    idx = 1
                    for option in item["options"]:
                        formhtml += f"""<input type=\"checkbox\" id=\"{item['id']}{idx}\" name=\"{item['id']}{idx}\" value="{option}">
                                        <label for=\"{item['id']}{idx}\">{option}</label><br>"""
                        idx += 1

            elif item["type"] == "title":
                formhtml += f"<h3>{item['value']}</h3>"
            elif item["type"] == "text":
                formhtml += f"<p>{item['value']}</p>"
            elif item["type"] == "textarea":
                defaulttext = item["default"] if "default" in item else ""
                formhtml += f"<textarea name=\"{item['name']}\" rows=\"{item['rows']}\" cols=\"{item['cols']}\">{defaulttext}</textarea><br>"
            elif item["type"] == "dropdown":
                formhtml += (
                    f"<label for=\"{item['id']}\">{item['label']}</label><br>"
                    f"<select name=\"{item['id']}\" name=\"{item['id']}\"><br>"
                )
                for option in item["options"]:
                    selected = ""
                    if "default" in item and item["default"] == option:
                        selected = " selected"
                    formhtml += f'<option name="{option}"{selected}>{option}</option>'
                formhtml += "</select><br>"

        formhtml += "<input type='submit' value='Submit'></form>"
        with open("form.html", "w") as f:
            f.write(formhtml)
        # return {"url": "http://localhost:8105/form.html"}

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get("content-type"))

        # refuse to receive non-json content
        if ctype != "application/json":
            self.send_response(400)
            self.end_headers()
            return
        # read the message and convert it into a python dictionary
        length = int(self.headers.get("content-length"))
        message = json.loads(self.rfile.read(length), object_pairs_hook=OrderedDict)
        self.create_form(message)

        self._set_headers()
        return

    def do_GET(self):
        if self.path.endswith("favicon.ico"):
            return
        elif "formresponsehandling" in self.path:
            query = urlparse(self.path).query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            self._set_headers()
            self.wfile.write(json.dumps(query_components).encode(encoding="utf-8"))
            return
        root = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "attended"
        )
        # print(self.path)
        if self.path == "/":
            filename = root + "/index.html"
        else:
            filename = root + self.path
        self._set_headers("html")
        self.end_headers()
        with open(filename, "rb") as fh:
            html = fh.read()
            # html = bytes(html, 'utf8')
            self.wfile.write(html)
        # self.wfile.write(self.getContent(self.getPath()))

    def getPath(self):
        if self.path == "/":
            content_path = Path.cwd() / Path("index.html")
        else:
            content_path = Path.cwd() / Path(self.path)
        return content_path

    def getContent(self, content_path):
        with open(content_path, mode="r", encoding="utf-8") as f:
            content = f.read()
        return bytes(content, "utf-8")


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def start_server(directory, port=8000):
    LOGGER.info("starting server atport=%s" % port)
    server = HTTPServer(("", port), Handler)
    server.serve_forever()


class Attended:
    attended_server = "http://localhost:8105"

    def start_server(self):
        self.daemon = threading.Thread(
            name="daemon_server", target=start_server, args=(".", 8105)
        )
        self.daemon.setDaemon(True)
        self.daemon.start()

    def __del__(self):
        LOGGER.info("Dialogs __del__")

    def request_response(self, formspec):
        LOGGER.info("Received: %s", formspec)
        self.start_server()
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        requests.post(self.attended_server, data=open(formspec, "rb"), headers=headers)
        # json_response = response.json()
        br = Browser()
        # br.open_available_browser(json_response["url"])
        br.open_available_browser(f"{self.attended_server}/form.html")
        br.set_window_position(200, 200)
        br.set_window_size(600, 800)
        location = None
        while True:
            location = br.get_location()
            if "formresponsehandling" in location:
                # content = br.get_source()
                break
            time.sleep(1)

        # headers = {"If-None-Match": "xyz", "Prefer": "wait=120"}
        # response_json = None
        # while True:
        #     response = requests.get(
        #         f"{self.attended_server}/requestresponse", headers=headers
        #     )
        #     # etag = response.headers.get("ETag")
        #     if response.status_code == 200:
        #         response_json = response.json()
        #     LOGGER.info(response)
        #     time.sleep(1)

        br.close_all_browsers()
        # http://localhost:8105/formresponsehandling?fname=John&lname=Doe
        location = location.replace("http://localhost:8105/formresponsehandling?", "")
        LOGGER.info("parsing: %s", location)
        # return response_json
        return dict(qc.split("=") for qc in location.split("&"))
        # return content
