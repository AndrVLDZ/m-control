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


from kekosik import Program

# название скрипта или действия (ключ из сообщения) -> что сделать
test_data = {
    "start/stop": (
        "C:\Program Files\PreSonus\Studio One 4\\Studio One.exe",
        ["space"],
    ),
    "Goto Next Мarker (Studio One)": (
        "C:\Program Files\PreSonus\Studio One 4\\Studio One.exe",
        ["shift + n"],
    ),
    "Goto Previous Мarker (Studio One)": (
        "C:\Program Files\PreSonus\Studio One 4\\Studio One.exe",
        ["shift + b"],
    ),
}

ENCODING = "utf-8"


def handle_message2(msg: bytes, scripts: dict[str, (str, list[str])]):
    # TODO: sanitize string
    print("Bytes in msg:", msg)
    message = str(msg, ENCODING)

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
        print("Host IP: " + str(host_ip_add))
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
                    # handle_message(str(data, "utf-8"))
                    handle_message2(data, test_data)
                    conn.sendall(data)


if __name__ == "__main__":
    print_logo()
    HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
    PORT = 9999  # Port to listen on (non-privileged ports are > 1023)
    CONNECTIONS_LIMIT = 1
    start_server(HOST, PORT, clients_limit=CONNECTIONS_LIMIT)