import time
import PySimpleGUI as sg
import pyautogui as pgui
from pynput import keyboard

action_duration = 0.1
hold_duration = 0.15
# pens_location = {'x':186, 'y':850}
# signature_location = {'x':275, 'y':774}
# candies_location = {'x':1318, 'y':354}
# ballon_location = {'x':1318, 'y':354}
stop_key = keyboard.Key.esc
set_location_key = keyboard.Key.space

sg.theme('Green')
elements = [['silver pens', 'signature'], ['candies'], ['ballons']]
modes = []
for element in elements:
    modes.append(element[0])
keys = []
for elements1 in elements:
    t =[]
    for element in elements1:
        t.append(f'-set_{element.replace(" ", "_")}_location-')
    keys.append(t)
locations = {}
for element in sum(elements, []):
    locations[element] = {'x':0, 'y':0}

layout = [[sg.Combo(values=modes, default_value=modes[0], readonly=True), sg.Button(button_text='change mode', key='-change_mode-')],
          [sg.Text('to set position of object press the corresponding button')],
          [sg.Text('then move your cursor to the object and press space')]]

for i in range(len(sum(elements,[]))):
    layout.append([sg.Button(button_text=f'set {sum(elements, [])[i]} location', key=sum(keys, [])[i])])
layout.append([sg.Button(button_text='start', key='-start-'), sg.Text('press esc to stop')])

window = sg.Window(title='Idleon Hours Saver', layout=layout, element_justification='center', finalize=True)

def set_location(key, location_dict):
    if key == set_location_key:
        location_dict['x'], location_dict['y'] = pgui.position()
        return False
    
def hide_elements(element_names):
    for element_name in element_names:
        window[element_name].hide_row()

def unhide_elements(element_names):
    for element_name in element_names:
        window[element_name].unhide_row()

def use_silver_pens():
    while is_running:
        pgui.moveTo(locations['silver pens']['x'], locations['silver pens']['y'], action_duration)
        pgui.click(duration=action_duration)
        pgui.moveTo(locations['signature']['x'], locations['signature']['y'], action_duration)
        pgui.click(duration=action_duration)
        pgui.click(duration=action_duration)

def use_candies():
    while is_running:                                           
        pgui.moveTo(locations['candies']['x'], locations['candies']['y'], action_duration)
        pgui.press('i')
        time.sleep(action_duration)
        pgui.mouseDown(duration=action_duration)
        time.sleep(hold_duration)
        pgui.mouseUp(duration=action_duration)
        time.sleep(action_duration)
        pgui.press('space')

def use_ballons():
    while is_running:
        pgui.moveTo(locations['ballons']['x'], locations['ballons']['y'], action_duration)
        pgui.mouseDown(duration=action_duration)
        time.sleep(hold_duration)
        pgui.mouseUp(duration=action_duration)

def stop(key):
    global is_running
    if key == stop_key:
        is_running = False

is_running = False
hide_elements(sum(keys[1:], []))

with keyboard.Listener(on_press=stop) as listener:
    while True:
        event, values = window.read()
        print(event, values)
        for i in range(len(sum(keys, []))):
            if event == sum(keys, [])[i]:
                # TODO remove multiple clicking bug
                with keyboard.Listener(on_press=lambda key:set_location(key,location_dict=locations[sum(elements, [])[i]])) as listener1:
                    listener1.join()              
        if event == '-start-':
            is_running = True
            for mode in modes:
                if values[0] == mode:
                    eval(f'use_{mode.replace(" ","_")}()')
        if event == '-change_mode-':
            hide_elements(sum(keys, [])+['-start-'])
            for i in range(len(modes)):
                if values[0] == modes[i]:
                    unhide_elements(keys[i])
            unhide_elements(['-start-'])
        if event == sg.WIN_CLOSED:
            break
        
window.close()