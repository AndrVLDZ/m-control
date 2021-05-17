#!/usr/bin/env python3

import socket


def print_logo(logo=""):
    LOGO_DAFAULT = """

   /\                 /\\
  / \\'._   (\_/)   _.'/ \\
 /_.''._'--('.')--'_.''._\\
 | \_ / `;=/ " \=;` \ _/ |
  \/ `\__|`\___/`|__/`  \/
   `      \(/|\)/        `
           " ` "
     DAW_Start_By_VLDZ 

"""
    if logo != "":
        print(logo)
    else:
        print(LOGO_DAFAULT)


BUF_SIZE = 1024

# variable where all connections stored
connections = []


def handle_message(data: str):
    # do smth.
    if data == "Hi from client!":
        print("===> Parsed msg: " + data)


def start_server(host_ip: str, port: int, clients_limit=0):
    print("[*] Starting server on {ip}:{port}...".format(ip=host_ip, port=port))
    # use the socket object without calling s.close().
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # used to associate the socket with a specific network interface and port number
        sock.bind((host_ip, port))
        sock.listen(clients_limit)
        while True:
            print("[*] Waiting for clients...")
            conn, addr = sock.accept()
            connections.append(addr)
            print("[*] Connected by => ", addr)
            with conn:
                while True:
                    if addr not in connections:
                        break
                    data = conn.recv(BUF_SIZE)
                    if not data or data == b"CLOSING":
                        print("[*] Closed connection with: ", conn.getpeername()[0])
                        connections.remove(addr)
                        break
                    # if some data recived then --> handle it
                    handle_message(str(data, "utf-8"))
                    conn.sendall(data)


if __name__ == "__main__":
    print_logo()
    HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
    PORT = 9999  # Port to listen on (non-privileged ports are > 1023)
    CONNECTIONS_LIMIT = 1
    start_server(HOST, PORT, clients_limit=CONNECTIONS_LIMIT)