import time
import json
import machine
from data_modules.object_handler import current_app, nav, keypad_state_manager, menu, menu_refresh, typer, keymap, display
from settings.backlight import backlight, backlight_pin
from settings.dark_mode import toggle_display_mode, display_mode_label
from process_modules import boot_up_data_update

def settings(db={}):
    display.clear_display()
    json_file = "/database/settings_app_list.json" 
    with open(json_file, "r") as file:
        data = json.load(file)
    
    settings_list = []
    
    for app in data:
        if app["visibility"]:
            settings_list.append(app["name"])

    menu.menu_list = settings_list
    menu.update()
    menu_refresh.refresh()
    try:
        while True:
            inp_menu = typer.start_typing()

            if inp_menu == "back":
                current_app[0] = "home"
                current_app[1] = "application_modules"
                break  
        
            elif inp_menu == "alpha" or inp_menu == "beta":
                keypad_state_manager(x=inp_menu)
                menu.update_buffer("")
            elif inp_menu == "off":
                boot_up_data_update.main()
                machine.deepsleep()
            elif inp_menu == "ok" and menu.menu_list[menu.menu_cursor] in ["dark_mode"]:
                toggle_display_mode()
               
            elif inp_menu == "ok" and menu.menu_list[menu.menu_cursor] in ["backlight"]:
                backlight()
            elif inp_menu == "ok":
                current_app[0] = menu.menu_list[menu.menu_cursor]
                current_app[1] = "settings"
                break
            menu.update_buffer(inp_menu)
            menu_refresh.refresh(state=nav.current_state())
            time.sleep(0.1)
    except Exception as e:
        print(f"Error: {e}")