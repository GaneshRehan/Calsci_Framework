import time
import json
import machine
from data_modules.object_handler import nav, keypad_state_manager, menu, menu_refresh, typer, keymap, display
from data_modules.object_handler import current_app
from process_modules import boot_up_data_update

def home(db={}):
    display.clear_display()
    json_file = "/database/application_modules_app_list.json" 
    with open(json_file, "r") as file:
        data = json.load(file)

    menu_list = []
    for app in data:
        if app["visibility"]:
            menu_list.append(app["name"])

    menu.menu_list=menu_list
    menu.update()
    menu_refresh.refresh()
    try:
        while True:
            inp = typer.start_typing()
            
            if inp == "back":
                pass
            
            elif inp == "alpha" or inp == "beta":                        
                keypad_state_manager(x=inp)
                menu.update_buffer("")
            elif inp =="ok":
                current_app[0]=menu.menu_list[menu.menu_cursor]
                break
            elif inp == "off":
                boot_up_data_update.main()
                machine.deepsleep()

            menu.update_buffer(inp)
            menu_refresh.refresh(state=nav.current_state())
            time.sleep(0.2)
    except Exception as e:
        print(f"Error: {e}")