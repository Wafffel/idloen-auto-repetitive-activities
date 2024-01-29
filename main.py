import time
import pyautogui as pgui
from pynput import keyboard
import sys

action_duration = 0.1
start_duration = 1
pen_location = {'x':200, 'y':850}
refresh_location = {'x':200, 'y':770}
move_to_pen_durtion = 1
close_key = keyboard.Key.esc

pgui.moveTo(pen_location['x'], pen_location['y'], move_to_pen_durtion)

exit_program = False
def on_press(key):
    global exit_program
    if key == close_key:
        exit_program = True 
        return False
with keyboard.Listener(on_press) as listener:
    time.sleep(start_duration)
    while exit_program == False:
        pgui.click(duration=action_duration)
        pgui.moveTo(refresh_location['x'], refresh_location['y'], action_duration)
        pgui.click(duration=action_duration)
        pgui.click(duration=action_duration)
        pgui.moveTo(pen_location['x'], pen_location['y'], action_duration)