import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app


def calculator(v1, v2):
    if len(v1) != len(v2):
        return 'e'
    
    n = len(v1)
    
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    
    # Other dimensions
    return result


def dot_product(db={}):
    form.input_list={"inp_0": "1+2+3", "inp_1": "4+5+6"}
    form.form_list = ["Vector 1:", "inp_0", "Vector 2:", "inp_1"]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0]="scientific_calculator"
            current_app[1]="application_modules"
            break
        

        if inp == "ok":
            v1 = list(map(int, form.input_list["inp_0"].split("+")))
            v2 = list(map(int, form.input_list["inp_1"].split("+")))
            print(v1)
            print(v2)

            res = calculator(v1, v2)      

            if len(form.form_list) == 4:
                if res != 'e':
                    form.form_list.append("Result is")
                    form.form_list.append(str(res))
                    form.form_list.append("scalar") 

                elif res == 'e':
                    form.form_list.append("Vectors must have")
                    form.form_list.append("same length for")
                    form.form_list.append("doing dot product")
                

            else:
                if res != 'e':
                    form.form_list[4] = "Result is"
                    form.form_list[5] = str(res)
                    form.form_list[6] = "scalar"

                elif res == 'e':
                    form.form_list[4] = "Vectors must have"
                    form.form_list[5] = "same lengthn for"
                    form.form_list[6] = "doing dot product"
                

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



