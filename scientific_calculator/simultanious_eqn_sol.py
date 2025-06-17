import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app


def solve_linear_equations(A, b):
    n = len(b)
    # Create augmented matrix [A|b]
    augmented = [[A[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    # Forward elimination
    for i in range(n):
        # Find pivot
        pivot = augmented[i][i]
        if abs(pivot) < 1e-10:
            # Look for non-zero pivot in later rows
            for k in range(i + 1, n):
                if abs(augmented[k][i]) > 1e-10:
                    augmented[i], augmented[k] = augmented[k], augmented[i]
                    pivot = augmented[i][i]
                    break
            else:
                raise ValueError("No unique solution exists")
        
        # Scale row to make pivot 1
        for j in range(i, n + 1):
            augmented[i][j] /= pivot
            
        # Eliminate column
        for k in range(n):
            if k != i:
                factor = augmented[k][i]
                for j in range(i, n + 1):
                    augmented[k][j] -= factor * augmented[i][j]
    
    # Extract solution
    solution = [augmented[i][n] for i in range(n)]
    solution = [0.0 if abs(x) < 1e-10 else round(x, 6) for x in solution]

    
    return solution

def calculator(n):
    while True:
        inp = typer.start_typing()
        if inp == "back":
            form.input_list={"inp_0": " "}
            form.form_list = ["Enter no. of variables", "inp_0"]
            form.update()
            display.clear_display()
            form_refresh.refresh()
            break
        elif inp == "ok":
            A = []
            b = []
            for i in range(1, n + 1):
                    a = list(map(int, form.input_list[f"inp_{i}"].split("+")))
                    A.append(a[:-1])
                    b.append(-1 * a[-1])

            result = solve_linear_equations(A, b)
            form.form_list = ["Values are:"]
            for i in range(n):
                form.form_list.append(f"Var{i + 1} = {result[i]:.6f}")
            
            


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




def simultanious_eqn_sol(db={}):
    form.input_list={"inp_0": " "}
    form.form_list = ["Enter no. of variables", "inp_0"]
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
            n = int(form.input_list["inp_0"])
            form.form_list = []
            for i in range(1, n + 1):
                form.input_list[f"inp_{i}"] = " "
                form.form_list.append(f"Enter eqn. {i}")
                form.form_list.append(f"inp_{i}")
            form.update()
            display.clear_display()
            form_refresh.refresh()
            
            calculator(n=n)        

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



