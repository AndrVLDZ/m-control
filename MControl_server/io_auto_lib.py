"""IO Automation library methods"""

from typing import AnyStr, Union

# Providers - libraries that are used for keyboard and mouse access and automation.
# >>> import pyautogui
import keyboard
import autoit

import subprocess
import os
from pathlib import Path

__encoding = "utf-8"


def which(program: str) -> Union[None, str]:
    def is_exe(fpath: AnyStr):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

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


class Program:
    def __init__(self, name: str, program_exe: str) -> None:
        self.name = name
        # TODO: check if file exists (path is correct)
        if Path(program_exe).is_file():
            self.exe_path = program_exe
        elif which(program_exe) is not None:
            self.exe_path = which(program_exe)
        else:
            raise FileNotFoundError(
                "Could not find *.exe file in the specified path", program_exe
            )

        # TODO: выснить нужен ли нам subprocess для чего-нибудь в будущем
        self.subproc = None

    def open_in_subprocess(self):
        self.subproc = subprocess.Popen([self.exe_path])

    def keypress(self, keyboard_cmd: str, release=True):
        keyboard.send(keyboard_cmd, do_press=True, do_release=release)

    def open_then_keypress(self, keyboard_cmd: str, release=True):
        self.open_in_subprocess()
        keyboard.send(keyboard_cmd, do_press=True, do_release=release)


if __name__ == "__main__":

    def run_programs_TEST(test_case: str):
        programs_exe = {
            # "Studio One 4": "C:\Program Files\PreSonus\Studio One 4\\Studio One.exe",
            # "Cyberpunk 2077": "C:\Games\Cyberpunk 2077\bin\x64\\Cyberpunk2077.exe",
            "Notepad": "notepad.exe",
        }

        progs = {}
        for name, path in programs_exe.items():
            progs[name] = Program(name, path)

        progs[test_case].open_then_keypress("ctrl + v")

    run_programs_TEST("Notepad")
