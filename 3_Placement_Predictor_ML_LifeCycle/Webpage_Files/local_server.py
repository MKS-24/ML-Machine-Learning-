import sys
sys.path.insert(0, "api")
from http.server import HTTPServer
from predict import handler as Api

class Local(Api):
    def do_GET(self):
        body = open("index.html", "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(body)

print("Open http://localhost:8000")
HTTPServer(("", 8000), Local).serve_forever()