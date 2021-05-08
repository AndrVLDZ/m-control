import autoit
import time
print("\nMouse 50 clicks")
clickCounter = 0
while clickCounter < 50:
    clickCounter += 1
    autoit.mouse_click("left")
    time.sleep(0.1)