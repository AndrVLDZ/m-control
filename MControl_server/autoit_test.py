import autoit
import time
import subprocess
import keyboard
from pywinauto.application import Application


from subprocess import Popen
from pywinauto import Desktop


Popen('calc.exe', shell=True)
dlg = Desktop(backend="uia").Calculator



# app = Application(backend="uia").start('notepad.exe')

# # describe the window inside Notepad.exe process
# dlg_spec = app.UntitledNotepad
# # wait till the window is really open
# actionable_dlg = dlg_spec.wait('visible')



# def top_foc(): 
#     app = Application().connect(path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
#     app = Application(backend='win32').connect(path="")
#     app.top_window().set_focus()
# top_foc()



# print("\nMouse 50 clicks")
# clickCounter
# B= 0
# while clickCounter < 50:
#     clickCounter += 1
#     autoit.mouse_click("left")
#     time.sleep(0.1)


# subprocess.Popen(["notepad.exe"])
# keyboard.send("shift + b")
# time.sleep(0.1)
# keyboard.send("Tvoya")

# autoit.run("notepad.exe")space
# autoit.win_wait_active("[CLASS:Notepad]", 3)
# autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")


# autoit.run("C:\ProgramData\Ableton\Live 10 Suite\Program\Ableton Live 10 Suite.exe")
# autoit.win_wait_active("C:\Program Files\PreSonus\Studio One 4\Studio One.exe")
# subprocess.Popen(
#     ["C:\ProgramData\Ableton\Live 10 Suite\Program\Ableton Live 10 Suite.exe"]
# )
 
def write():
    process = subprocess.Popen(["notepad.exe"])
    keyboard.send("ctrl + v")
    process.wait()

# write()

def write_studio():
    subprocess.call(["C:\Program Files\Google\Chrome\Application\chrome.exe"])
    # process = subprocess.Popen(["C:\Program Files\Google\Chrome\Application\chrome.exe"])
    keyboard.send("space") 
 
# write_studio()



# START = autoit.run("C:\Program Files\PreSonus\Studio One 4\Studio One.exe")
# # autoit.win_wait_active("C:\Program Files\PreSonus\Studio One 4\Studio One.exe")
# keyboard.send("space", do_press=True, do_release=True)
# autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")


# subprocess.call(["Notepad"])

# subprocess.call(["C:\Program Files\PreSonus\Studio One 4\\Studio One.exe"])
