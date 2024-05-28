from http.server import BaseHTTPRequestHandler
from tasks import Tasks
import json, os, sys

BASE_DIR = os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) != "" else "."

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            tasks = Tasks(f"{BASE_DIR}/tasks.tsk")
            response = open(f"{BASE_DIR}/static/index.html", "r").read().format(body=tasks.html())
            
        elif self.path == "/static/style.css":
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            response = open(f"{BASE_DIR}/static/style.css", "r").read()
            
        elif self.path == "/static/script.js":
            self.send_response(200)
            self.send_header("Content-type", "text/javascript")
            response = open(f"{BASE_DIR}/static/script.js", "r").read()
            
        else:
            self.send_response(404)
            response = "404 Not Found"
        
        self.end_headers()
        self.wfile.write(response.encode())
            
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Invalid JSON")
            return None
        
        tasks = Tasks(f"{BASE_DIR}/tasks.tsk")
        
        if self.path == "/getcode":
            source = tasks.getcode(data["date"])
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            response = json.dumps({"source": source.strip("\n")})
            
        elif self.path == "/save":
            tasks.update(data["date"], "\n"+data["source"]+"\n")
            parsed = tasks.parse("---\n"+data["source"])
            html = tasks.html_day(parsed)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            response = json.dumps({"html": html})
                
        elif self.path == "/add":
            tasks.add("\n"+data["source"]+"\n---")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            response = json.dumps({"html": tasks.html()})
                
        else:
            self.send_response(404)
            response = "404 Not Found"

        self.end_headers()
        self.wfile.write(response.encode())