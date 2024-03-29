import time
import PySimpleGUI as sg
import pyautogui as pgui
from pynput import keyboard

action_duration = 0.1
hold_duration = 0.15
destroy_boss_duration = 6
collect_loot_duration = 3
load_player_duration = 3
stop_key = keyboard.Key.esc
set_location_key = keyboard.Key.space

sg.theme('Green')
elements = [['silver pens', 'signature'], ['candies'], ['ballons'], ['boss refresh', 'start of loot', 'end of loot'], ['click'], ['quick anvil deposit', 'produce tab', 'codex button', 'quick ref', 'quick ref anvil', 'players button', 'player 1', 'player 2', 'player 3', 'player 4', 'player 5', 'player 6', 'left player tab arrow', 'right player tab arrow']]
modes = [element[0] for element in elements]
keys = []
for elements1 in elements:
    t =[f'-set_{element.replace(" ", "_")}_location-' for element in elements1]
    keys.append(t)
locations = {}
for element in sum(elements, []):
    locations[element] = {'x':0, 'y':0}
 
with open('positions.txt', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        position=line[:-1].split(';')
        locations[position[0]] = {'x':int(position[1]), 'y':int(position[2]) }

print(locations)
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

def stop(key):
    global is_running
    if key == stop_key:
        is_running = False

def use_silver_pens():
    while is_running:
        pgui.moveTo(locations['silver pens']['x'], locations['silver pens']['y'], action_duration)
        pgui.click(duration=action_duration)
        pgui.moveTo(locations['signature']['x'], locations['signature']['y'], action_duration)
        pgui.click(duration=action_duration)
        pgui.click(duration=action_duration)

def use_candies():
    pgui.moveTo(locations['candies']['x'], locations['candies']['y'], action_duration)
    while is_running:                                                   
        pgui.press('i')
        time.sleep(action_duration)
        pgui.mouseDown(duration=action_duration)
        time.sleep(hold_duration)
        pgui.mouseUp(duration=action_duration)
        time.sleep(action_duration)
        pgui.press('space')

def use_ballons():
    pgui.moveTo(locations['ballons']['x'], locations['ballons']['y'], action_duration)
    while is_running:        
        pgui.mouseDown(duration=action_duration)
        time.sleep(hold_duration)
        pgui.mouseUp(duration=action_duration)

def use_boss_refresh():
    while is_running:
        pgui.moveTo(locations['boss refresh']['x'], locations['boss refresh']['y'], action_duration)
        pgui.click(duration=action_duration)
        time.sleep(destroy_boss_duration)
        pgui.moveTo(locations['start of loot']['x'], locations['start of loot']['y'], action_duration)
        pgui.mouseDown(duration=action_duration)
        pgui.moveTo(locations['end of loot']['x'], locations['end of loot']['y'], collect_loot_duration)
        pgui.mouseUp(duration=action_duration)

def use_click():
    pgui.moveTo(locations['click']['x'], locations['click']['y'], action_duration)
    while is_running:
        pgui.click(duration=action_duration)

def single_anvil_claim():
    pgui.moveTo(locations['codex button']['x'], locations['codex button']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations['quick ref']['x'], locations['quick ref']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations['quick ref anvil']['x'], locations['quick ref anvil']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations['produce tab']['x'], locations['produce tab']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations['quick anvil deposit']['x'], locations['quick anvil deposit']['y'], action_duration)
    pgui.click(duration=action_duration)

def swap_player(number):
    pgui.moveTo(locations['players button']['x'], locations['players button']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations[f'player {number+1}']['x'], locations[f'player {number+1}']['y'], action_duration)
    pgui.click(duration=action_duration)
    time.sleep(load_player_duration)
    pgui.press('space')

def use_quick_anvil_deposit():
    global is_running
    is_running = False
    pgui.moveTo(locations['players button']['x'], locations['players button']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations['left player tab arrow']['x'], locations['left player tab arrow']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.press('esc')
    for i in range(6):
        swap_player(i)
        single_anvil_claim()
    pgui.moveTo(locations['players button']['x'], locations['players button']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.moveTo(locations['right player tab arrow']['x'], locations['right player tab arrow']['y'], action_duration)
    pgui.click(duration=action_duration)
    pgui.press('esc')
    for i in range(4):
        swap_player(i)
        single_anvil_claim()

is_running = False
hide_elements(sum(keys[1:], []))

with keyboard.Listener(on_press=stop) as listener:
    while True:
        event, values = window.read()
        print(event, values)
        for i in range(len(sum(keys, []))):
            if event == sum(keys, [])[i]:
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

with open('positions.txt', 'w') as f:
    for key, value in locations.items():
        f.write(f'{key};{value["x"]};{value["y"]}\n')