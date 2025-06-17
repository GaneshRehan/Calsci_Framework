import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def npr_calculator(n, r):
    if r < 0 or r > n:
        return 0
    if r == 0:
        return 1
    
    # Calculate nPr as n * (n-1) * ... * (n-r+1)
    result = 1
    for i in range(n, n-r, -1):
        result *= i
    return result

def nPr(db={}):
    form.input_list={"inp_0": " "}
    form.form_list = ["Enter n and r", "inp_0"]
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
            n, r = map(int, form.input_list["inp_0"].split("+"))
            
            nPr = npr_calculator(n, r)
            if len(form.form_list) == 2:
                form.form_list.append(f"nPr is:") 
                form.form_list.append(f"{nPr}")
            else:
                form.form_list[-2] = f"nPr is:"
                form.form_list[-1] = f"{nPr}"

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



