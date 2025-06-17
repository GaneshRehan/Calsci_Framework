import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app


def calculator(v1, v2):
    # Ensure vectors have the same length
    if len(v1) != len(v2):
        return -1
    
    n = len(v1)
    
    # Case: 2D vectors (return scalar)
    if n == 2:
        return [[v1[0] * v2[1] - v1[1] * v2[0]], "scalar"]
    
    # Case: 3D vectors (return vector)
    if n == 3:
        x = v1[1] * v2[2] - v1[2] * v2[1]
        y = v1[2] * v2[0] - v1[0] * v2[2]
        z = v1[0] * v2[1] - v1[1] * v2[0]
        return [[x, y, z], "vector"]
    
    # Other dimensions
    return -2


def cross_product(db={}):
    form.input_list={"inp_0": " ", "inp_1": " "}
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
                if res != -1 and res != -2:
                    form.form_list.append("Resulting vector")
                    form.form_list.append(" ".join(str(x) for x in res[0]))
                    form.form_list.append(res[1]) 

                elif res == -1:
                    form.form_list.append("Cross product not")
                    form.form_list.append("possible different")
                    form.form_list.append("component vectors")
                else:
                    form.form_list.append("Cross product not")
                    form.form_list.append("possible above 3D")
                    form.form_list.append("vectors")

            else:
                if res != -1 and res != -2:
                    form.form_list[4] = "Resulting vector"
                    form.form_list[5] = " ".join(str(x) for x in res[0])
                    form.form_list[6] = res[1]

                elif res == -1:
                    form.form_list[4] = "Cross product not"
                    form.form_list[5] = "possible different "
                    form.form_list[4] = "component vectors"
                else:
                    form.form_list[4] = ("Cross product not")
                    form.form_list[5] = ("possible above 3D")
                    form.form_list[6] = "vectors"

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



