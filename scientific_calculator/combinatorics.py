import time
import json
import machine
from data_modules.object_handler import current_app, nav, keypad_state_manager, menu, menu_refresh, typer, keymap, display
from settings.backlight import backlight, backlight_pin
from process_modules import boot_up_data_update

def combinatorics(db={}):
    display.clear_display()
    json_file = "/database/combinatorics_app_list.json" 
    with open(json_file, "r") as file:
        data = json.load(file)
    
    combinatorics_app_list = []
    

    for app in data:
        if app["visibility"]:
            combinatorics_app_list.append(app["name"])

    combinatorics_app_list.sort()

    menu.menu_list=combinatorics_app_list
    menu.update()
    menu_refresh.refresh()
    try:
        while True:
            inp_menu = typer.start_typing()

            if inp_menu == "back":
                current_app[0]="scientific_calculator"
                current_app[1]="application_modules"
                break
        
            elif inp_menu == "alpha" or inp_menu == "beta":
                keypad_state_manager(x=inp_menu)
                menu.update_buffer("")
            elif inp_menu == "off":
                boot_up_data_update.main()
                machine.deepsleep()
            elif inp_menu =="ok":
                current_app[0]=menu.menu_list[menu.menu_cursor]
                current_app[1] = "combinatorics"
                break
            menu.update_buffer(inp_menu)
            menu_refresh.refresh(state=nav.current_state())
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")