import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def is_valid_matrix(matrix, rows, cols):
    if not matrix or len(matrix) != rows or not matrix[0]:
        return False
    
    if rows != cols:
        return False
    
    for row in matrix:
        if len(row) != cols:
            return False
        
    
    return True, (rows, cols)

def lu_decomposition_finder(matrix, rows, cols):
    is_valid = is_valid_matrix(matrix, rows, cols)
    if not is_valid:
        pass
    
    n = rows
    L = [[0.0 for _ in range(n)] for _ in range(n)]
    U = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        L[i][i] = 1.0
    
    matrix = [row[:] for row in matrix]
    
    for k in range(n):
        U[k][k] = matrix[k][k]
        for j in range(k + 1, n):
            U[k][j] = matrix[k][j]
        
        for i in range(k + 1, n):
            if abs(U[k][k]) < 1e-10:
                raise ValueError("Matrix is singular or nearly singular")
            L[i][k] = matrix[i][k] / U[k][k]
            for j in range(k, n):
                matrix[i][j] -= L[i][k] * U[k][j]
    
    return L, U


def calculator(r, c):
    while True:
        inp = typer.start_typing()
        if inp == "back":
            form.input_list={"inp_0": " "}
            form.form_list = ["Enter matrix dimension", "r + c", "inp_0"]
            form.update()
            display.clear_display()
            form_refresh.refresh()
            break

        
        if inp == "ok":
            matrix = []
            for i in range(1, r + 1):
                    a = list(map(int, form.input_list[f"inp_{i}"].split("+")))
                    matrix.append(a)
            
            l, u = lu_decomposition_finder(matrix, r, c)
                
            form.form_list = [f"LU Decomposition:", "L Matrix:"]
            for row in l:
                t = [round(x, 4) for x in row]
                form.form_list.append(" ".join(str(x) for x in t))

            form.form_list.append("U Matrix:")
            for row in u:
                t = [round(x, 4) for x in row]
                form.form_list.append(" ".join(str(x) for x in t))


            
            
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



def lu_decomposition(db={}):
    form.input_list={"inp_0": " "}
    form.form_list = ["Enter matrix dimension", "r + c", "inp_0"]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0]="matrix_operations"
            current_app[1]="scientific_calculator"
            break
        

        if inp == "ok":
            r, c = list(map(int, form.input_list[f"inp_0"].split("+")))
            if r != c:
                form.form_list = ["LU Decomposition", "not possible"]
                form.update()
                display.clear_display()
                form_refresh.refresh()
            else:
                form.form_list = []
                for i in range(1, r + 1):
                    form.input_list[f"inp_{i}"] = " "
                    form.form_list.append(f"Enter row no. {i}")
                    form.form_list.append(f"inp_{i}")
                form.update()
                display.clear_display()
                form_refresh.refresh()
                
                calculator(r, c)
                
            
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



