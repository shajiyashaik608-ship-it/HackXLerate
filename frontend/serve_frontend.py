import os
import sys
import http.server
import urllib.request
import urllib.error

PORT = 5173
BACKEND_URL = "http://127.0.0.1:8000"
FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
PREVIEW_FILE = os.path.join(FRONTEND_DIR, "preview.html")

class HealthSaathiFrontendHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        self.proxy_or_serve("GET")

    def do_POST(self):
        self.proxy_or_serve("POST")

    def do_PUT(self):
        self.proxy_or_serve("PUT")

    def do_PATCH(self):
        self.proxy_or_serve("PATCH")

    def do_DELETE(self):
        self.proxy_or_serve("DELETE")

    def proxy_or_serve(self, method):
        path = self.path
        # Proxy backend endpoints
        if path.startswith("/api/") or path.startswith("/health") or path.startswith("/readiness") or path.startswith("/docs") or path.startswith("/openapi.json"):
            target_url = f"{BACKEND_URL}{path}"
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else None

            # Prepare proxy request
            req = urllib.request.Request(target_url, data=body, method=method)
            for k, v in self.headers.items():
                if k.lower() not in ("host", "content-length"):
                    req.add_header(k, v)

            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    self.send_response(resp.status)
                    for k, v in resp.headers.items():
                        if k.lower() not in ("content-length", "transfer-encoding"):
                            self.send_header(k, v)
                    resp_body = resp.read()
                    self.send_header("Content-Length", str(len(resp_body)))
                    self.end_headers()
                    self.wfile.write(resp_body)
            except urllib.error.HTTPError as e:
                self.send_response(e.code)
                for k, v in e.headers.items():
                    if k.lower() not in ("content-length", "transfer-encoding"):
                        self.send_header(k, v)
                err_body = e.read()
                self.send_header("Content-Length", str(len(err_body)))
                self.end_headers()
                self.wfile.write(err_body)
            except Exception as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"error": "Backend unavailable"}')
            return

        # Otherwise serve preview.html / static frontend files
        if os.path.exists(PREVIEW_FILE):
            with open(PREVIEW_FILE, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Frontend preview file not found.")

if __name__ == "__main__":
    server_address = ("127.0.0.1", PORT)
    ServerClass = getattr(http.server, "ThreadingHTTPServer", http.server.HTTPServer)
    httpd = ServerClass(server_address, HealthSaathiFrontendHandler)
    print(f"Health Saathi Frontend Server running at: http://localhost:{PORT}/")
    print(f"Proxying API calls to Backend at: {BACKEND_URL}")
    httpd.serve_forever()
