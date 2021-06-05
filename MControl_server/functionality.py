from abc import ABCMeta, abstractmethod
from typing import Callable, Union

from typing import AnyStr, Union

# Providers - libraries that are used for keyboard and mouse access and automation.
# >>> import pyautogui
# >>> import pywinauto
# >>> import autoit

import subprocess
import os
from pathlib import Path


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

        # TODO: выяснить нужен ли нам subprocess для чего-нибудь в будущем
        self.subproc = None

        st_info = subprocess.STARTUPINFO()
        st_info.wShowWindow = subprocess.STARTF_USESHOWWINDOW
        self.startupinfo = st_info

    def open_in_subprocess(self):
        self.subproc = subprocess.Popen([self.exe_path], startupinfo=self.startupinfo)


# ---------------------- >
class AbstractKeyboardProvider(metaclass=ABCMeta):
    @abstractmethod
    def press(self, hotkey: str, press=True, release=True):
        pass

    @abstractmethod
    def send_hotkey(self, hotkey: str, press=True, release=True):
        pass

    @abstractmethod
    def send_text(self, text: str):
        pass

    @abstractmethod
    def add_hotkey(self, hotkey_lambda: Callable[[str], None]):
        pass

    @abstractmethod
    def wait(self, key: Union[str, None]):
        pass


# ---------------------- >
import keyboard


class KeyboardProvider(AbstractKeyboardProvider):
    def __init__(self, prog: Program):
        self.program = prog

    def press(self, hotkey: str, press=True, release=True):
        raise NotImplemented

    def send_hotkey(self, hotkey_as_str: str, press=True, release=True):
        self.program.open_in_subprocess()
        keyboard.send(hotkey=hotkey_as_str, do_press=press, do_release=release)

    def send_text(self, text: str, delay_seconds: int = 0):
        raise NotImplemented

    def add_hotkey(self, hotkey_lambda: Callable[[str], None]):
        raise NotImplemented

    def wait(self, key: Union[str, None]):
        raise NotImplemented


if __name__ == "__main__":
    p = Program("Notepad", "notepad.exe")

    keyboard_provider = KeyboardProvider(prog=p)
    keyboard_provider.send_hotkey("ctrl+v")
