from abc import ABCMeta, abstractmethod
from typing import Callable, Union

# Providers - libraries that are used for keyboard and mouse access and automation.
# >>> import pyautogui
# >>> import pywinauto
# >>> import autoit
import keyboard

import subprocess
from pathlib import Path
from src.utils.common import which


class Program:
    def __init__(self, name: str, program_exe: str) -> None:
        self.name = name
        if Path(program_exe).is_file():
            self.exe_path = program_exe
        elif which(program_exe) is not None:
            self.exe_path = which(program_exe)
        else:
            raise FileNotFoundError(
                "Could not find *.exe file in the specified path", program_exe
            )

        # save subprocess instance to work with it later e.g. (self.subproc.close, ...)
        self.subproc = None

        st_info = subprocess.STARTUPINFO()
        st_info.wShowWindow = subprocess.STARTF_USESHOWWINDOW
        self.startupinfo = st_info

    def open_in_subprocess(self):
        self.subproc = subprocess.Popen([self.exe_path], startupinfo=self.startupinfo)


class AbstractKeyboardProvider(metaclass=ABCMeta):
    @abstractmethod
    def send_hotkey(self, hotkey: str, press=True, release=True):
        pass

    @abstractmethod
    def press(self, hotkey: str, press=True, release=True):
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


class KeyboardProvider(AbstractKeyboardProvider):
    def __init__(self, prog: Program):
        self.program = prog

    def send_hotkey(self, hotkey_as_str: str, press=True, release=True):
        self.program.open_in_subprocess()
        keyboard.send(hotkey=hotkey_as_str, do_press=press, do_release=release)

    def press(self, hotkey: str, press=True, release=True):
        raise NotImplemented

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
