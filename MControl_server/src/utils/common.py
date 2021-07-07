from typing import AnyStr, Optional
import os
from pathlib import Path


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


def which(program: str) -> Optional[str]:
    def is_exe(file_path: AnyStr):
        return os.path.isfile(file_path) and os.access(file_path, os.X_OK)

    filepath, _filename = os.path.split(program)
    if filepath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            if is_exe(exe_file := os.path.join(path, program)):
                return exe_file

    return None


if __name__ == "__main__":
    raise NotImplemented
