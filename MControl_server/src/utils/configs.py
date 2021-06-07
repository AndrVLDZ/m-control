from dataclasses import dataclass


@dataclass
class DBConfig:
    db_folder_name: str = "data"
    passwd_encoding: str = "utf-8"
    do_encryption: bool = False


# TCP server configuration parameters
@dataclass
class ServerConfig:
    ascii_logo: str
    msg_encoding: str = "utf-8"
    buf_size: int = 1024
    disconnection_keyword: str = "CLOSING"
