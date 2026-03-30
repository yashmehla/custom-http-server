import socket
import os
import threading
import mimetypes

HOST = "0.0.0.0"
PORT = 8080
ROOT = "."
BUFFER_SIZE = 8192

# Preload small files (reduces disk I/O latency)
CACHE = {}

def load_file(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
        return data, mime
    except:
        return None, None

def get_response(path):
    if path == "/":
        path = "/index.html"

    full_path = os.path.join(ROOT, path.lstrip("/"))

    if full_path in CACHE:
        body, mime = CACHE[full_path]
    else:
        body, mime = load_file(full_path)
        if body and len(body) < 1024 * 1024:  # cache only small files (<1MB)
            CACHE[full_path] = (body, mime)

    if body:
        headers = (
            "HTTP/1.1 200 OK\r\n"
            f"Content-Type: {mime}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode()
        return headers, body
    else:
        body = b"404 Not Found"
        headers = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n\r\n"
        ).encode()
        return headers, body


def handle_client(conn):
    try:
        request = conn.recv(BUFFER_SIZE)
        if not request:
            return

        # Fast request parsing (no heavy parsing)
        try:
            path = request.split(b" ")[1].decode()
        except:
            path = "/"

        headers, body = get_response(path)
        conn.sendall(headers)
        conn.sendall(body)
    finally:
        conn.close()


def start():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(128)  # higher backlog

        print(f"Serving on http://{HOST}:{PORT}")

        while True:
            conn, _ = server.accept()
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    start()
