import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def complex_modulus(z):
    """Calculate modulus of a complex number: |a + bi| = sqrt(a^2 + b^2)"""
    return (z[0]**2 + z[1]**2)**0.5

def modulous(db={}):
    form.input_list={"inp_0": " ", "inp_1": " "}
    form.form_list = ["Enter complex number:", "inp_0"]
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
            z1 = list(map(int, form.input_list["inp_0"].split("+")))

            
            mod = complex_modulus(z1)
            if len(form.form_list) == 2:
                form.form_list.append(f"Modulous is:") 
                form.form_list.append(f"{mod}")
            else:
                form.form_list[-2] = f"Modulous is:"
                form.form_list[-1] = f"{mod}"

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



