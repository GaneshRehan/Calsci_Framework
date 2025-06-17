import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def complex_divide(z1, z2):
    """Divide two complex numbers: (a + bi)/(c + di) = ((ac + bd) + (bc - ad)i)/(c^2 + d^2)"""
    denominator = z2[0]**2 + z2[1]**2
    if denominator == 0:
        raise ValueError("Division by zero is not allowed")
    real = (z1[0] * z2[0] + z1[1] * z2[1]) / denominator
    imag = (z1[1] * z2[0] - z1[0] * z2[1]) / denominator
    return (real, imag)

def division(db={}):
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

            
            z3 = complex_divide(z1, z2)
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



