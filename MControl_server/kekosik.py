from typing import List
import keyboard
import autoit
# import pyautogui
import subprocess
import time
from pathlib import Path

ENCODING = "utf-8" 


class Program:
    def __init__(self, name: str, exe_path: str) -> None:
        self.name = name
        # TODO: check if file exists (path is correct)
        if Path(exe_path).is_file():
            self.exe_path = exe_path
        else:
            raise FileNotFoundError(
                "Could not find *.exe file in the specified path", exe_path
            )

        # TODO: выснить нужен ли нам subprocess для чего-нибудь в будущем
        self.subprocess = None

    def open_in_subprocess(self):
        self.subprocess = subprocess.Popen([self.exe_path])

    def keypress(self, keyboard_cmd: str, release=True):
        keyboard.send(keyboard_cmd, do_press=True, do_release=release)

    def open_then_keypress(self, keyboard_cmd: str, release=True):
        self.open_in_subprocess()
        keyboard.send(keyboard_cmd, do_press=True, do_release=release)


def handle_message(msg: bytes, scripts: dict[str, (str, list[str])]):
    # TODO: sanitize string
    print("Bytes in msg:", msg)
    message = str(msg, ENCODING).removesuffix("\r\n")

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


def simple_test():
    programs_exe = {
        "Studio One 4": "C:\Program Files\PreSonus\Studio One 4\\Studio One.exe",
        "Cyberpunk 2077": "C:\Games\Cyberpunk 2077\bin\x64\\Cyberpunk2077.exe",
    }
    progs = {}
    for name, path in programs_exe.items():
        progs[name] = Program(name, path)

    progs["Studio One 4"].open_then_keypress("space")


def handle_event_msg(data):
    if str(data, "utf-8") == "s\r\n":
        subprocess.Popen(["C:\Program Files\PreSonus\Studio One 4\\Studio One.exe"])
        keyboard.send("space", do_press=True, do_release=True)
        print("\nKeypress event 'Strat/Stop'")
    elif str(data, "utf-8") == "b\r\n":
        subprocess.Popen(["C:\Program Files\PreSonus\Studio One 4\\Studio One.exe"])
        keyboard.send("shift + b")
        print("\nKeypress event 'Goto Previous Мarker'")
    elif str(data, "utf-8") == "n\r\n":
        subprocess.Popen(["C:\Program Files\PreSonus\Studio One 4\\Studio One.exe"])
        keyboard.send("shift + n")
        print("\nKeypress event 'Goto Next Мarker'")

    elif str(data, "utf-8") == "c100\r\n":
        #        subprocess.Popen(['C:\Games\Cyberpunk 2077\bin\x64\\Cyberpunk2077.exe'])
        print("\nMouse 1000 clicks")
        clickCounter = 0
        while clickCounter < 100:
            clickCounter += 1
            autoit.mouse_down("left")
            time.sleep(0.1)
            autoit.mouse_up("left")
            time.sleep(0.05) 

    elif str(data, "utf-8") == "":
        print("\nClient request to disconnect")

    else:
        print("\nJust a msg")
        print(str(data, "utf-8"))


if __name__ == "__main__":
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

    handle_message(b"start/stop", test_data)