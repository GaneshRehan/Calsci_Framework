import utime as time  # type: ignore
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, spreadsheet_buffer, spreadsheet_refresh, keymap, current_app

from process_modules import boot_up_data_update


def spreadsheet(db={}):
    display.clear_display()
    spreadsheet_refresh.update_scroll()
    spreadsheet_refresh.refresh()

    spreadsheet_buffer.in_input_mode = False
    spreadsheet_buffer.temp_value = ""

    while True:
        inp = typer.start_typing()

        if inp == "back":
            spreadsheet_buffer.save_to_file()
            spreadsheet_buffer.in_input_mode = False
            spreadsheet_buffer.temp_value = ""
            current_app[0] = "home"
            current_app[1] = "application_modules"
            break

        elif inp == "off":
            spreadsheet_buffer.in_input_mode = False
            spreadsheet_buffer.temp_value = ""
            boot_up_data_update.main()
            machine.deepsleep()

        elif inp in ["alpha", "beta"]:
            keypad_state_manager(x=inp)
            continue

        if spreadsheet_buffer.in_input_mode:
            if inp == "ok":
                spreadsheet_buffer.update_cell(spreadsheet_buffer.temp_value.strip())
                spreadsheet_buffer.in_input_mode = False
                spreadsheet_buffer.temp_value = ""
            elif inp == "nav_b":
                spreadsheet_buffer.temp_value = spreadsheet_buffer.temp_value[:-1]
            elif inp == "AC":
                spreadsheet_buffer.temp_value = ""
            elif len(inp) == 1:
                spreadsheet_buffer.temp_value += inp


        else:
            if inp == "ok":
                spreadsheet_buffer.in_input_mode = True
                spreadsheet_buffer.temp_value = spreadsheet_buffer.buffer[spreadsheet_buffer.current_cell]
            elif inp in ["nav_u", "nav_d", "nav_l", "nav_r"]:
                direction = {
                    "nav_u": "up",
                    "nav_d": "down",
                    "nav_l": "left",
                    "nav_r": "right"
                }[inp]
                spreadsheet_buffer.move(direction)




        spreadsheet_refresh.update_scroll()
        spreadsheet_refresh.refresh()
        time.sleep(0.15)

