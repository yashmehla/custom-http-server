import socket
import os
from datetime import datetime

HOST = "0.0.0.0"
PORT = 8080
STATIC_DIR = "static"

def http_response(status, body=b"", content_type="text/html"):
    headers = [
        f"HTTP/1.1 {status}",
        f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}",
        "Server: CustomPythonServer",
        f"Content-Length: {len(body)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode() + body

def handle_request(req):
    try:
        line = req.split(b"\r\n")[0].decode()
        method, path, _ = line.split()

        if method != "GET":
            return http_response("405 Method Not Allowed", b"Method not allowed")

        if path == "/":
            path = "/index.html"

        file_path = os.path.join(STATIC_DIR, path.lstrip("/"))

        if not os.path.exists(file_path):
            return http_response("404 Not Found", b"Not found")

        with open(file_path, "rb") as f:
            body = f.read()

        content_type = "text/html"
        if file_path.endswith(".css"): content_type = "text/css"
        if file_path.endswith(".js"): content_type = "application/javascript"
        if file_path.endswith(".png"): content_type = "image/png"

        return http_response("200 OK", body, content_type)

    except Exception as e:
        return http_response("500 Internal Server Error", str(e).encode())

def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Serving on http://{HOST}:{PORT}")

        while True:
            conn, _ = s.accept()
            with conn:
                req = conn.recv(4096)
                resp = handle_request(req)
                conn.sendall(resp)

if __name__ == "__main__":
    start()
