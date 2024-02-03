import time
import PySimpleGUI as sg
import pyautogui as pgui
from pynput import keyboard

action_duration = 0.1
start_duration = 1
pen_location = {'x':200, 'y':850}
signature_location = {'x':200, 'y':770}
stop_key = keyboard.Key.space
set_location_key = keyboard.Key.space

sg.theme('Green')

layout = [[sg.Text('to set location of something press the corresponding button')],
          [sg.Text('then move your cursoor to the object and press space')],
          [sg.Button('set pens location')],
          [sg.Button('set signature location')],
          [sg.Button('start'), sg.Text('press space to stop')]]

window = sg.Window('Idleon Hours Saver', layout)

def set_pen_location(key):
    if key == set_location_key:
        pen_location['x'], pen_location['y'] = pgui.position()
        return False

def set_signature_location(key):
    if key == set_location_key:
        signature_location['x'], signature_location['y'] = pgui.position()
        return False

def stop(key):
    global is_running
    if key == stop_key:
        is_running = False

is_running = False

with keyboard.Listener(on_press=stop) as listener:
    while True:
        event, values = window.read()
        print(event, values)
        if event == 'set pens laction':
            # TODO remove multiple clicking bug
            with keyboard.Listener(on_press=set_pen_location) as listener1:
                listener1.join()
        if event == 'set signature location':
            with keyboard.Listener(on_press=set_signature_location) as listener1:
                listener1.join()
        if event == 'start':
            is_running = True
            while is_running:
                pgui.moveTo(pen_location['x'], pen_location['y'], action_duration)
                pgui.click(duration=action_duration)
                pgui.moveTo(signature_location['x'], signature_location['y'], action_duration)
                pgui.click(duration=action_duration)
                pgui.click(duration=action_duration)
        if event == sg.WIN_CLOSED:
            break

window.close()