import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def gcd_calculator(a, b):
    while b:
        a, b = b, a % b
    return a

def gcd(db={}):
    form.input_list={"inp_0": " "}
    form.form_list = ["Enter 2 numbers:", "inp_0"]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0]="combinatorics"
            current_app[1]="scientific_calculator"
            break
        

        if inp == "ok":
            a, b = map(int, form.input_list["inp_0"].split("+"))
            
            gcd = gcd_calculator(a, b)
            if len(form.form_list) == 2:
                form.form_list.append(f"GCD is:") 
                form.form_list.append(f"{gcd}")
            else:
                form.form_list[-2] = f"GCD is:"
                form.form_list[-1] = f"{gcd}"

            form.update()
            display.clear_display()
            form_refresh.refresh()
            
       
        if inp == "alpha" or inp == "beta":
            keypad_state_manager(x=inp)
            form.update_buffer("")

        if inp == "off":
            boot_up_data_update.main()
            machine.deepsleep()
        if inp not in ["alpha", "beta", "ok"]:
            form.update_buffer(inp)
        form_refresh.refresh(state=nav.current_state())
        time.sleep(0.15)



