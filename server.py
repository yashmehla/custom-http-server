from socket import *

HOST = "0.0.0.0"
PORT = 8080

server = socket(AF_INET, SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Serving on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    request = conn.recv(1024)

    response = b"""HTTP/1.1 200 OK

Hello, world
"""
    conn.sendall(response)
    conn.close()
