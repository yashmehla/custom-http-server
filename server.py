from socket import *
import os

HOST = "0.0.0.0"
PORT = 8080

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Serving on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024)

    if os.path.exists("index.html"):
        with open("index.html", "rb") as f:
            body = f.read()
        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: text/html\r\n"
        response += f"Content-Length: {len(body)}\r\n".encode()
        response += b"\r\n"
        response += body
    else:
        body = b"404 Not Found"
        response = b"HTTP/1.1 404 Not Found\r\n"
        response += b"Content-Type: text/plain\r\n"
        response += f"Content-Length: {len(body)}\r\n".encode()
        response += b"\r\n"
        response += body

    conn.sendall(response)
    conn.close()
