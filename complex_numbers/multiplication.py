import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def complex_multiply(z1, z2):
    """Multiply two complex numbers: (a + bi)(c + di) = (ac - bd) + (ad + bc)i"""
    real = z1[0] * z2[0] - z1[1] * z2[1]
    imag = z1[0] * z2[1] + z1[1] * z2[0]
    return (real, imag)

def multiplication(db={}):
    form.input_list={"inp_0": " ", "inp_1": " "}
    form.form_list = ["Enter complex number1:", "inp_0", "Enter complex number2:", "inp_1"]
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
            z2 = list(map(int, form.input_list["inp_1"].split("+")))

            
            z3 = complex_multiply(z1, z2)
            if len(form.form_list) == 4:
                form.form_list.append(f"Result is:") 
                form.form_list.append(f"{z3[0]} {"+" if z3[1] >= 0 else ''}{z3[1]}i")
            else:
                form.form_list[-2] = f"Result is:"
                form.form_list[-1] = f"{z3[0]} {"+" if z3[1] >= 0 else ''}{z3[1]}i"

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



