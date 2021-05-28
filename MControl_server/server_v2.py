#!/usr/bin/env python3

import socket
from typing import Any, Dict, List, Tuple
from data_privers import test_data
from io_auto_lib import Program


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
    print(logo if logo else LOGO_DAFAULT)


__encoding = "utf-8"
__buf_size = 1024
# variable where all connections stored
connections: List[Any] = []


def handle_message(msg: bytes, scripts: Dict[str, Tuple[str, List[str]]]):
    # TODO: sanitize string
    print("Bytes in msg:", msg)
    message = str(msg, __encoding)

    if message in scripts.keys():
        program_exe_path, commands = scripts[message]
        print(
            "Got message:",
            message,
            "\n  => doing:",
            commands,
            "\n  on",
            program_exe_path,
        )
        # do actual work
        program = Program("Some program", program_exe_path)
        program.open_then_keypress(commands[0])
    else:
        print("Message:", message, "did not match to specified scripts names")


def start_server(host_ip: str, port: int, clients_limit=0):
    print("[*] Starting server on {ip}:{port}...".format(ip=host_ip, port=port))
    # use the socket object without calling s.close().
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # used to associate the socket with a specific network interface and port number
        sock.bind((host_ip, port))
        sock.listen(clients_limit)
        host_ip_add = socket.gethostbyname(socket.getfqdn())
        print("Host IP:", host_ip_add)
        while True:
            print("[*] Waiting for clients...")
            conn, addr = sock.accept()
            connections.append(addr)
            print("[*] Connected by =>", addr)
            with conn:
                while True:
                    if addr not in connections:
                        break
                    data = conn.recv(__buf_size)
                    if not data or data == b"CLOSING":
                        print("[*] Closed connection with:", conn.getpeername()[0])
                        connections.remove(addr)
                        break
                    # if some data recived then --> handle it
                    handle_message(data, test_data)
                    conn.sendall(data)


if __name__ == "__main__":
    print_logo()
    HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
    PORT = 9999  # Port to listen on (non-privileged ports are > 1023)
    CONNECTIONS_LIMIT = 1
    start_server(HOST, PORT, clients_limit=CONNECTIONS_LIMIT)
