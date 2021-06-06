from typing import AnyStr, Union, Optional
import os
from models import get_printable_users
from dataclasses import dataclass
from pathlib import Path

# ___________________
from rich.console import Console

# rich text console
console = Console()
console.print(get_printable_users())
# ___________________


@dataclass
class DBConfig:
    db_folder_name: str = "data"
    passwd_encoding: str = "utf-8"
    do_encryption: bool = False


def check_file(full_path: str) -> Optional[str]:
    if Path(full_path).is_file():
        return full_path
    else:
        raise FileNotFoundError(f"Could not find file with filename: '{full_path}'")


def check_dir(full_path: str) -> Optional[str]:
    if Path(full_path).is_dir():
        return full_path
    else:
        raise IOError(f"Invalid directory specified: '{full_path}'")


def get_project_dir() -> AnyStr:
    return os.path.dirname(os.path.realpath(__file__))


def which(program: str) -> Union[None, str]:
    def is_exe(file_path: AnyStr):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    fpath, _fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None
