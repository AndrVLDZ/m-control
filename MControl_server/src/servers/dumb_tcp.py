#!/usr/bin/env python3

import socket
from typing import Any, Dict, List, Tuple


class MessageHandler:
    def __init__(self, scripts_from_db: Dict[str, Tuple[str, List[str]]]):
        self.data = scripts_from_db

    def handle_msg(self, message: str):
        if message in self.data.keys():
            program_exe_path, commands = self.data[message]
            print(
                "Got message:",
                message,
                "\n  => doing:",
                commands,
                "\n  on",
                program_exe_path,
            )
            # TODO:
            #  impl. actual PAYLOAD mechanism = access provider of functionality
            #  (keyboard, GUI, mouse... automation)
        else:
            print("Message:", message, "did not match to specified scripts names")


class DumbTCP:
    def __init__(self, host: str, port: int, handler: MessageHandler):
        self.host_ip = host
        self.port_number = port
        # connections storage
        self.connected: Dict[str, Any] = dict()
        self.handler = handler

    def close_conn(self, address: str):
        if address not in self.connected.keys():
            print(
                "[*] Failed attempt to close already dropped connection with:", address
            )
            return False

        self.connected.pop(address)
        print("[*] Closed connection with:", address)
        return True

    def start_server(self):
        print(f"[*] Starting server on {self.host_ip}:{self.port_number}...")
        # use the socket object without calling s.close().
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # used to associate the socket with a specific network interface and port number
            sock.bind((self.host_ip, self.port_number))
            sock.listen()
            host_ip_add = socket.gethostbyname(socket.getfqdn())
            print("LAN host IP:", host_ip_add)
            while True:
                print("[*] Waiting for clients...")
                conn, address = sock.accept()
                # store new connection info
                self.connected[address] = conn
                # and send message to debug
                print("[*] Connected by =>", address)
                with conn:
                    while True:
                        # if disconnected before - break loop
                        if address not in self.connected.keys():
                            break

                        # read data from connected client
                        data: bytes = conn.recv(config.buf_size)
                        # disconnect when got `disconnection keyword` or "empty" msg
                        # (by default in most libs client sends empty msg as disconnection flag)
                        if (
                            not data
                            or data.decode(config.msg_encoding)
                            == config.disconnection_keyword
                        ):
                            self.close_conn(address)
                            break

                        # if some data received then --> handle it
                        self.handler.handle_msg(
                            message=data.decode(config.msg_encoding)
                        )
                        conn.sendall(data)


if __name__ == "__main__":
    from src.utils.configs import ServerConfig

    # Название скрипта или действия (ключ из сообщения) -> что сделать
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
        "Notepad": (
            "notepad.exe",
            ["ctrl + v"],
        ),
    }

    # TODO: we need to get data from DB provider
    dumbHandler = MessageHandler(test_data)

    LOGO_V1: str = """

       /\                 /\\
      / \\'._   (\_/)   _.'/ \\
     /_.''._'--('.')--'_.''._\\
     | \_ / `;=/ " \=;` \ _/ |
      \/ `\__|`\___/`|__/`  \/
       `      \(/|\)/        `
               " ` "
         DAW_Start_By_VLDZ 

    """
    # create default server config
    config = ServerConfig(ascii_logo=LOGO_V1)

    # Standard loop back interface address (localhost)
    HOST = "0.0.0.0"
    # Port to listen on (non-privileged ports are > 1023)
    PORT = 9999
    dumbTCP = DumbTCP(HOST, PORT, dumbHandler)
    dumbTCP.start_server()
