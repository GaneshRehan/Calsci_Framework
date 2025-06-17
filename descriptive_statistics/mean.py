import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def calculate_mean(numbers):
    """Calculate the mean (average) of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def mean(db={}):
    form.input_list={"inp_0": " "}
    form.form_list = ["Enter data:", "inp_0"]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0]="descriptive_statistics"
            current_app[1]="scientific_calculator"
            break
        

        if inp == "ok":
            data = list(map(int, form.input_list["inp_0"].split("+")))

            
            mean = calculate_mean(data)
            if len(form.form_list) == 2:
                form.form_list.append(f"Mean is:") 
                form.form_list.append(f"{mean}")
            else:
                form.form_list[-2] = f"Mean is:"
                form.form_list[-1] = f"{mean}"

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



