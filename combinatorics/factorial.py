import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def factorial_calculator(n):
    
    if n == 0 or n == 1:
        return 1
   
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def factorial(db={}):
    form.input_list={"inp_0": " "}
    form.form_list = ["Enter number:", "inp_0"]
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
            n = int(form.input_list["inp_0"])
            
            n_factorial = factorial_calculator(n)
            if len(form.form_list) == 2:
                form.form_list.append(f"Factorial of {n} is:") 
                form.form_list.append(f"{n_factorial}")
            else:
                form.form_list[-2] = f"Factorial of {n} is:"
                form.form_list[-1] = f"{n_factorial}"

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



