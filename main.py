import time
import PySimpleGUI as sg
import pyautogui as pgui
from pynput import keyboard

action_duration = 0.1
hold_duration = 0.15
pens_location = {'x':200, 'y':850}
signature_location = {'x':200, 'y':770}
candy_location = {'x':200, 'y':850}
ballon_location = {'x':200, 'y':770}
stop_key = keyboard.Key.esc
set_location_key = keyboard.Key.space

sg.theme('Green')
modes = ['silver pens', 'candies', 'ballon']

layout = [[sg.Combo(values=modes, default_value=modes[0], readonly=True), sg.Button(button_text='change mode', key='-change_mode-')],
          [sg.Text('to set position of object press the corresponding button')],
          [sg.Text('then move your cursor to the object and press space')],
          [sg.Button(button_text='set pens location', key='-set_pens_location-')],
          [sg.Button(button_text='set signature location', key='-set_signature_location-')],
          [sg.Button(button_text='set candy location', key='-set_candy_location-')],
          [sg.Button(button_text='set ballon location', key='-set_ballon_location-')],
          [sg.Button(button_text='start', key='-start-'), sg.Text('press esc to stop')]]

window = sg.Window(title='Idleon Hours Saver', layout=layout, element_justification='center', finalize=True)

def set_pens_location(key):
    if key == set_location_key:
        pens_location['x'], pens_location['y'] = pgui.position()
        return False

def set_signature_location(key):
    if key == set_location_key:
        signature_location['x'], signature_location['y'] = pgui.position()
        return False
    
def set_candy_location(key):
    if key == set_location_key:
        candy_location['x'], candy_location['y'] = pgui.position()
        return False
    
def set_ballon_location(key):
    if key == set_location_key:
        ballon_location['x'], ballon_location['y'] = pgui.position()
        return False

def stop(key):
    global is_running
    if key == stop_key:
        is_running = False

is_running = False
window['-set_candy_location-'].hide_row()
window['-set_ballon_location-'].hide_row()

with keyboard.Listener(on_press=stop) as listener:
    while True:
        event, values = window.read()
        print(event, values)
        if event == '-set_pens_location-':
            # TODO remove multiple clicking bug
            with keyboard.Listener(on_press=set_pens_location) as listener1:
                listener1.join()
        if event == '-set_signature_location-':
            with keyboard.Listener(on_press=set_signature_location) as listener1:
                listener1.join()
        if event == '-set_candy_location-':
            with keyboard.Listener(on_press=set_candy_location) as listener1:
                listener1.join()
        if event == '-set_ballon_location-':
            with keyboard.Listener(on_press=set_ballon_location) as listener1:
                listener1.join()                
        if event == '-start-':
            is_running = True
            if values[0] == modes[0]:
                while is_running:
                    pgui.moveTo(pens_location['x'], pens_location['y'], action_duration)
                    pgui.click(duration=action_duration)
                    pgui.moveTo(signature_location['x'], signature_location['y'], action_duration)
                    pgui.click(duration=action_duration)
                    pgui.click(duration=action_duration)
            if values[0] == modes[1]:
                while is_running:
                    pgui.press('i')
                    pgui.moveTo(candy_location['x'], candy_location['y'], action_duration)
                    pgui.mouseDown(duration=action_duration)
                    time.sleep(hold_duration)
                    pgui.mouseUp(duration=action_duration)
                    time.sleep(action_duration)
                    pgui.press('space')
            if values[0] == modes[2]:
                while is_running:
                    pgui.moveTo(ballon_location['x'], ballon_location['y'], action_duration)
                    pgui.mouseDown(duration=action_duration)
                    time.sleep(hold_duration)
                    pgui.mouseUp(duration=action_duration)
        if event == '-change_mode-':
            window['-set_pens_location-'].hide_row()         
            window['-set_signature_location-'].hide_row()
            window['-set_candy_location-'].hide_row()
            window['-set_ballon_location-'].hide_row()
            window['-start-'].hide_row()
            if values[0] == modes[0]:
                window['-set_pens_location-'].unhide_row()
                window['-set_signature_location-'].unhide_row()                
            if values[0] == modes[1]:
                window['-set_candy_location-'].unhide_row()
            if values[0] == modes[2]:
                window['-set_ballon_location-'].unhide_row()
            window['-start-'].unhide_row()
        if event == sg.WIN_CLOSED:
            break

print(f'pen location {pens_location["x"]} {pens_location["y"]}')
print(f'signature location {signature_location["x"]} {signature_location["y"]}')
print(f'candy location {candy_location["x"]} {candy_location["y"]}')
window.close()