import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, text, nav, text_refresh, typer, keypad_state_manager, keypad_state_manager_reset, current_app
from process_modules import boot_up_data_update
def calculate(db={}):
    keypad_state_manager_reset()
    display.clear_display()
    text.all_clear()
    text_refresh.refresh()
    try:
        while True:

            x = typer.start_typing()
            # print(f"x = {x}")
            if x == "back":
                current_app[0]="home"
                current_app[1] = "application_modules"
                break
            
            if x == "ans" and text.text_buffer[0] != "𖤓":
                try:
                    res = str(eval(text.text_buffer[:text.text_buffer_nospace]))
                except Exception as e:
                    res = "Invalid Input"
                text.all_clear()
                display.clear_display()
                text.update_buffer(res)

            elif x == "alpha" or x == "beta":                        
                keypad_state_manager(x=x)
                text.update_buffer("")

            elif x == "off":
                boot_up_data_update.main()
                machine.deepsleep()

            elif x != "ans":
                text.update_buffer(x)

            if text.text_buffer[0] == "𖤓":
                display.clear_display()
                text.all_clear()

            text_refresh.refresh(state=nav.current_state())
            time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
