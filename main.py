import time
import PySimpleGUI as sg
import pyautogui as pgui
from pynput import keyboard

action_duration = 0.1
hold_duration = 0.5
pen_location = {'x':200, 'y':850}
signature_location = {'x':200, 'y':770}
items_location = {'x':200, 'y':850}
candy_location = {'x':200, 'y':850}
claim_location = {'x':200, 'y':770}
stop_key = keyboard.Key.space
set_location_key = keyboard.Key.space

sg.theme('Green')
modes = ['silver pens', 'candies']

layout = [[sg.Combo(values=modes, default_value=modes[0], readonly=True), sg.Button(button_text='change mode', key='-change_mode-')],
          [sg.Text('to set position of object press the corresponding button')],
          [sg.Text('then move your cursor to the object and press space')],
          [sg.Button(button_text='set pens location', key='-set_pens_location-')],
          [sg.Button(button_text='set signature location', key='-set_signature_location-')],
          [sg.Button(button_text='set items location', key='-set_items_location-')],
          [sg.Button(button_text='set candy location', key='-set_candy_location-')],
          [sg.Button(button_text='set claim location', key='-set_claim_location-')],
          [sg.Button(button_text='start', key='-start-'), sg.Text('press space to stop')]]

window = sg.Window(title='Idleon Hours Saver', layout=layout, element_justification='center', finalize=True)

def set_pen_location(key):
    if key == set_location_key:
        pen_location['x'], pen_location['y'] = pgui.position()
        return False

def set_signature_location(key):
    if key == set_location_key:
        signature_location['x'], signature_location['y'] = pgui.position()
        return False
    
def set_items_location(key):
    if key == set_location_key:
        items_location['x'], items_location['y'] = pgui.position()
        return False
    
def set_candy_location(key):
    if key == set_location_key:
        candy_location['x'], candy_location['y'] = pgui.position()
        return False

def set_claim_location(key):
    if key == set_location_key:
        claim_location['x'], claim_location['y'] = pgui.position()
        return False

def stop(key):
    global is_running
    if key == stop_key:
        is_running = False

is_running = False
window['-set_items_location-'].hide_row()
window['-set_candy_location-'].hide_row()
window['-set_claim_location-'].hide_row()

with keyboard.Listener(on_press=stop) as listener:
    while True:
        event, values = window.read()
        print(event, values)
        if event == '-set_pens_location-':
            # TODO remove multiple clicking bug
            with keyboard.Listener(on_press=set_pen_location) as listener1:
                listener1.join()
        if event == '-set_signature_location-':
            with keyboard.Listener(on_press=set_signature_location) as listener1:
                listener1.join()
        if event == '-set_items_location-':
            with keyboard.Listener(on_press=set_items_location) as listener1:
                listener1.join()
        if event == '-set_candy_location-':
            with keyboard.Listener(on_press=set_candy_location) as listener1:
                listener1.join()
        if event == '-set_claim_location-':
            with keyboard.Listener(on_press=set_claim_location) as listener1:
                listener1.join()
        if event == '-start-':
            is_running = True
            if values[0] == modes[0]:
                while is_running:
                    pgui.moveTo(pen_location['x'], pen_location['y'], action_duration)
                    pgui.click(duration=action_duration)
                    pgui.moveTo(signature_location['x'], signature_location['y'], action_duration)
                    pgui.click(duration=action_duration)
                    pgui.click(duration=action_duration)
            if values[0] == modes[1]:
                while is_running:
                    pgui.moveTo(items_location['x'], items_location['y'], action_duration)
                    pgui.click(duration=action_duration)
                    pgui.moveTo(candy_location['x'], candy_location['y'], action_duration)
                    pgui.mouseDown(duration=action_duration)
                    time.sleep(hold_duration)
                    pgui.mouseUp(duration=action_duration)
                    pgui.moveTo(claim_location['x'], claim_location['y'], action_duration)
                    pgui.click(duration=action_duration)
        if event == '-change_mode-':
            window['-set_pens_location-'].hide_row()         
            window['-set_signature_location-'].hide_row()
            window['-set_items_location-'].hide_row()
            window['-set_candy_location-'].hide_row()
            window['-set_claim_location-'].hide_row()
            window['-start-'].hide_row()
            if values[0] == modes[0]:
                window['-set_pens_location-'].unhide_row()
                window['-set_signature_location-'].unhide_row()                
            if values[0] == modes[1]:
                window['-set_items_location-'].unhide_row()
                window['-set_candy_location-'].unhide_row()
                window['-set_claim_location-'].unhide_row()
            window['-start-'].unhide_row()
        if event == sg.WIN_CLOSED:
            break

window.close()