import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def complex_conjugate(z):
    """Calculate conjugate of a complex number: conj(a + bi) = a - bi"""
    return (z[0], -z[1])

def conjugate(db={}):
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

            
            z2 = complex_conjugate(z1)
            if len(form.form_list) == 2:
                form.form_list.append(f"Conjugate is:") 
                form.form_list.append(f"{z2[0]} {"+" if z2[1] >= 0 else ''}{z2[1]}i")
            else:
                form.form_list[-2] = f"Conjugate is:"
                form.form_list[-1] = f"{z2[0]} {"+" if z2[1] >= 0 else ''}{z2[1]}i"

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



