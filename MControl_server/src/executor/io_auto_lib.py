"""IO Automation library methods"""

from typing import AnyStr, Union

# Providers - libraries that are used for keyboard and mouse access and automation.
# >>> import pyautogui, autoit
import keyboard

import subprocess
from pathlib import Path
from src.utils.common import which


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

        # TODO: выяснить нужен ли нам subprocess для чего-нибудь в будущем
        self.subproc = None

    def open_in_subprocess(self):
        self.subproc = subprocess.Popen([self.exe_path])

    def keypress(self, keyboard_cmd: str, release=True):
        # keyboard.send(keyboard_cmd, do_press=True, do_release=release)
        raise NotImplemented

    def open_then_keypress(self, keyboard_cmd: str, release=True):
        self.open_in_subprocess()
        keyboard.send(keyboard_cmd, do_press=True, do_release=release)


if __name__ == "__main__":

    def run_programs_test(test_case: str):
        programs_exe = {
            # TODO: add more tests
            "Notepad": "notepad.exe",
        }

        progs = {}
        for name, path in programs_exe.items():
            progs[name] = Program(name, path)

        progs[test_case].open_then_keypress("ctrl + v")

    run_programs_test("Notepad")
