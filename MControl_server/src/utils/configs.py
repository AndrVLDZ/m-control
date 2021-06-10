from dataclasses import dataclass
from typing import Optional

from .common import check_dir, check_file
import os


@dataclass
class DBConfig:
    db_filename: str
    db_folder: str
    db_provider: str = "sqlite"
    db_encryption: bool = False
    passwd_encoding: str = "utf-8"
    user_passwd_secret: str = "Scoopty-whoop; Whoopity-scoop"
    create_new_db: bool = False
    
    def check_db_path(self) -> str:
        checked_folder = check_dir(self.db_folder)
        if self.create_new_db:
            return os.path.join(checked_folder, self.db_filename)
        return check_file(os.path.join(checked_folder, self.db_filename))


SERVER_LOGO = """

       /\                 /\\
      / \\'._   (\_/)   _.'/ \\
     /_.''._'--('.')--'_.''._\\
     | \_ / `;=/ " \=;` \ _/ |
      \/ `\__|`\___/`|__/`  \/
       `      \(/|\)/        `
               " ` "
         DAW_Start_By_VLDZ 

"""


# TCP server configuration parameters
@dataclass
class ServerConfig:
    ascii_logo: str = SERVER_LOGO
    msg_encoding: str = "utf-8"
    buf_size: int = 1024
    disconnection_keyword: str = "CLOSING"


if __name__ == "__main__":
    print("This is configs: nothing to test here")
