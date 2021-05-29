import autoit
import time
import subprocess
import keyboard 

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

# autoit.run("notepad.exe")
# autoit.win_wait_active("[CLASS:Notepad]", 3)
# autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")
 

 
# autoit.run("C:\ProgramData\Ableton\Live 10 Suite\Program\Ableton Live 10 Suite.exe")
# autoit.win_wait_active("C:\Program Files\PreSonus\Studio One 4\Studio One.exe")
subprocess.Popen(["C:\ProgramData\Ableton\Live 10 Suite\Program\Ableton Live 10 Suite.exe"])
# keyboard.write("space", do_press=True, do_release=True) 
autoit.control_send(" ")
 
 
# START = autoit.run("C:\Program Files\PreSonus\Studio One 4\Studio One.exe")
# # autoit.win_wait_active("C:\Program Files\PreSonus\Studio One 4\Studio One.exe")
# keyboard.send("space", do_press=True, do_release=True)
# autoit.control_send("[CLASS:Notepad]", "Edit1", "hello world{!}")


# subprocess.call(["Notepad"])

# subprocess.call(["C:\Program Files\PreSonus\Studio One 4\\Studio One.exe"])                                                                                          

