import time
import pyautogui as pgui
from pynput import keyboard

action_duration = 0.1
start_duration = 1
pen_location = {'x':200, 'y':850}
signature_location = {'x':200, 'y':770}
close_key = keyboard.Key.esc
stop_start_key = keyboard.Key.f4
set_pen_location_key = keyboard.Key.f1
set_signature_location_key = keyboard.Key.f2

is_running = False
exit_program = False
def on_press(key):
    global exit_program
    global is_running
    if key == close_key:
        exit_program = True 
        return False
    if key == set_pen_location_key:
        pen_location['x'], pen_location['y'] = pgui.position()
    if key == set_signature_location_key:
        signature_location['x'], signature_location['y'] = pgui.position()
    if key == stop_start_key:
        is_running = not is_running
        
print('f1 - set silver pens location')
print('f2 - set place for a signature location')
print('f4 - start/stop')
print('esc - close app')

with keyboard.Listener(on_press) as listener:
    time.sleep(start_duration)
    while exit_program == False:
        if is_running:
            pgui.moveTo(pen_location['x'], pen_location['y'], action_duration)
            pgui.click(duration=action_duration)
            pgui.moveTo(signature_location['x'], signature_location['y'], action_duration)
            pgui.click(duration=action_duration)
            pgui.click(duration=action_duration)