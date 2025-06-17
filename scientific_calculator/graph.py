import framebuf # type: ignore
import math
import utime as time  # type:ignore
from data_modules.object_handler import display, form, nav, text, text_refresh, form_refresh, typer, keypad_state_manager, keypad_state_manager_reset
from data_modules.object_handler import current_app
import gc

eval_globals = {
    # Functions
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    'atan': math.atan,
    'atan2': math.atan2,
    'ceil': math.ceil,
    'copysign': math.copysign,
    'degrees': math.degrees,
    'exp': math.exp,
    'fabs': math.fabs,
    'floor': math.floor,
    'fmod': math.fmod,
    'frexp': math.frexp,
    'ldexp': math.ldexp,
    'log': math.log,
    'modf': math.modf,
    'pow': math.pow,
    'radians': math.radians,
    'sqrt': math.sqrt,
    'trunc': math.trunc,
    
    # Constants
    'pi': math.pi,
    'e': math.e,
}


def format_number(value):
    pi_multiple = value / math.pi
    if abs(pi_multiple - round(pi_multiple)) < 0.001:  
        multiple = round(pi_multiple)
        if multiple == 0:
            return "0 "
        elif multiple == 1:
            return "pi "
        elif multiple == -1:
            return "-pi "
        else:
            return f"{multiple}*pi "
    return f"{value:.2f} "

class SmallCharacters:
    Chr3x5_data = {
        "x": [0x05, 0x02, 0x05],  # x 
        "m": [0x07, 0x06, 0x07],  # m 
        "i": [0x00, 0x17, 0x00],  # i 
        "n": [0x07, 0x04, 0x07],  # n 
        "a": [0x17, 0x15, 0x1F],  # a 
        "_": [0x01, 0x01, 0x01],  # _ 
        " ": [0x00, 0x00, 0x00],  # Space
        "y": [0x1D, 0x05, 0x1F],  # y 
    }

    @classmethod
    def get_char(cls, char):
        return cls.Chr3x5_data.get(char, [0x1F, 0x1F, 0x1F])  # Default to solid block if char not found


def draw_small_text(fb, text, x, y):
    """Draw text using the 3x5 font on the framebuffer."""
    for char in text:
        char_data = SmallCharacters.get_char(char)
        for col in range(3):  # 3 pixels wide
            byte = char_data[col]
            for row in range(5):  # 5 pixels tall
                if byte & (1 << (4 - row)):  # Bit is set (1)
                    fb.pixel(x + col, y + row, 1)
        x += 4  # Move 4 pixels to the right for the next character (3 width + 1 space)


def graph(db={}):
    print("start of graph", gc.mem_free())
    keypad_state_manager_reset()
    global display, form, form_refresh, typer, nav, current_app, eval_globals
    form.input_list={"inp_0": "x*sin(x) ", "inp_1": "-20 ", "inp_2": "20 ", "inp_3": "-10 ", "inp_4": "10 "}
    form.form_list=["enter function:f(x)", "inp_0", "enter x_min:", "inp_1", "enter x_max:", "inp_2", "enter y_min:", "inp_3", "enter y_max:", "inp_4"]
    form.update()
    form_refresh.refresh()

    buffer1 = bytearray((128 * 64) // 8)
    fb1 = framebuf.FrameBuffer(buffer1, 128, 64, framebuf.MONO_VLSB)

    while True:
        inp = typer.start_typing()
        if inp == "back":
            del buffer1, fb1
            current_app[0]="scientific_calculator"
            current_app[1] = "application_modules"
            break

        elif inp == "ok":
            plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                         x_min=eval(form.inp_list()["inp_1"], eval_globals), 
                         x_max=eval(form.inp_list()["inp_2"], eval_globals), 
                         y_min=eval(form.inp_list()["inp_3"], eval_globals), 
                         y_max=eval(form.inp_list()["inp_4"], eval_globals), 
                         width=128, height=64)
            display.clear_display()
            display.graphics(buffer1)
            print("after plotting", gc.mem_free())
            new_x_min = eval(form.inp_list()["inp_1"], eval_globals)
            new_x_max = eval(form.inp_list()["inp_2"], eval_globals)
            new_y_min = eval(form.inp_list()["inp_3"], eval_globals)
            new_y_max = eval(form.inp_list()["inp_4"], eval_globals)


            while True:
                inp_breaker = typer.start_typing()
                if inp_breaker == "+":
                    x_range = eval(form.inp_list()["inp_2"], eval_globals) - eval(form.inp_list()["inp_1"], eval_globals)
                    y_range = eval(form.inp_list()["inp_4"], eval_globals) - eval(form.inp_list()["inp_3"], eval_globals)
                    
                    x_center = (eval(form.inp_list()["inp_1"], eval_globals) + eval(form.inp_list()["inp_2"], eval_globals)) / 2
                    y_center = (eval(form.inp_list()["inp_3"], eval_globals) + eval(form.inp_list()["inp_4"], eval_globals)) / 2
                    
                    new_x_range = x_range * 0.75
                    new_y_range = y_range * 0.75
                    
                    new_x_min = x_center - new_x_range/2
                    new_x_max = x_center + new_x_range/2
                    new_y_min = y_center - new_y_range/2
                    new_y_max = y_center + new_y_range/2
                    
                    form.input_list["inp_1"] = format_number(new_x_min)
                    form.input_list["inp_2"] = format_number(new_x_max)
                    form.input_list["inp_3"] = format_number(new_y_min)
                    form.input_list["inp_4"] = format_number(new_y_max)

                    fb1.fill(0)
                    plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                            x_min=new_x_min, x_max=new_x_max, 
                            y_min=new_y_min, y_max=new_y_max, 
                            width=128, height=64)
                    display.clear_display()
                    display.graphics(buffer1)
                    print("after plotting", gc.mem_free())


                elif inp_breaker == "-":
                    x_range = eval(form.inp_list()["inp_2"], eval_globals) - eval(form.inp_list()["inp_1"], eval_globals)
                    y_range = eval(form.inp_list()["inp_4"], eval_globals) - eval(form.inp_list()["inp_3"], eval_globals)
                    
                    x_center = (eval(form.inp_list()["inp_1"], eval_globals) + eval(form.inp_list()["inp_2"], eval_globals)) / 2
                    y_center = (eval(form.inp_list()["inp_3"], eval_globals) + eval(form.inp_list()["inp_4"], eval_globals)) / 2
                    
                    new_x_range = x_range * 1.25
                    new_y_range = y_range * 1.25
                    
                    new_x_min = x_center - new_x_range/2
                    new_x_max = x_center + new_x_range/2
                    new_y_min = y_center - new_y_range/2
                    new_y_max = y_center + new_y_range/2
                    
                    form.input_list["inp_1"] = format_number(new_x_min)
                    form.input_list["inp_2"] = format_number(new_x_max)
                    form.input_list["inp_3"] = format_number(new_y_min)
                    form.input_list["inp_4"] = format_number(new_y_max)

                    fb1.fill(0)
                    plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                            x_min=new_x_min, x_max=new_x_max, 
                            y_min=new_y_min, y_max=new_y_max, 
                            width=128, height=64)
                    display.clear_display()
                    display.graphics(buffer1)
                    print("after plotting", gc.mem_free())


                elif inp_breaker == "nav_u":
                    y_range = eval(form.inp_list()["inp_4"], eval_globals) - eval(form.inp_list()["inp_3"], eval_globals)
    
                    shift = y_range * 0.2
                    new_y_min = eval(form.inp_list()["inp_3"], eval_globals) + shift
                    new_y_max = eval(form.inp_list()["inp_4"], eval_globals) + shift
                    
                    new_x_min = eval(form.inp_list()["inp_1"], eval_globals)
                    new_x_max = eval(form.inp_list()["inp_2"], eval_globals)

                    form.input_list["inp_3"] = format_number(new_y_min)
                    form.input_list["inp_4"] = format_number(new_y_max)

                    fb1.fill(0)
                    plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                            x_min=new_x_min, x_max=new_x_max, 
                            y_min=new_y_min, y_max=new_y_max, 
                            width=128, height=64)
                    display.clear_display()
                    display.graphics(buffer1)
                    print("after plotting", gc.mem_free())


                elif inp_breaker == "nav_d":
                    y_range = eval(form.inp_list()["inp_4"], eval_globals) - eval(form.inp_list()["inp_3"], eval_globals)
    
                    shift = y_range * 0.2

                    new_y_min = eval(form.inp_list()["inp_3"], eval_globals) - shift
                    new_y_max = eval(form.inp_list()["inp_4"], eval_globals) - shift
                    
                    new_x_min = eval(form.inp_list()["inp_1"], eval_globals)
                    new_x_max = eval(form.inp_list()["inp_2"], eval_globals)
                    
                    form.input_list["inp_3"] = format_number(new_y_min)
                    form.input_list["inp_4"] = format_number(new_y_max)

                    fb1.fill(0)
                    plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                            x_min=new_x_min, x_max=new_x_max, 
                            y_min=new_y_min, y_max=new_y_max, 
                            width=128, height=64)
                    display.clear_display()
                    display.graphics(buffer1)
                    print("after plotting", gc.mem_free())


                elif inp_breaker == "nav_l":
                    x_range = eval(form.inp_list()["inp_2"], eval_globals) - eval(form.inp_list()["inp_1"], eval_globals)

                    shift = x_range * 0.2

                    new_x_min = eval(form.inp_list()["inp_1"], eval_globals) - shift
                    new_x_max = eval(form.inp_list()["inp_2"], eval_globals) - shift

                    new_y_min = eval(form.inp_list()["inp_3"], eval_globals)
                    new_y_max = eval(form.inp_list()["inp_4"], eval_globals)

                    form.input_list["inp_1"] = format_number(new_x_min)
                    form.input_list["inp_2"] = format_number(new_x_max)

                    fb1.fill(0)
                    plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                            x_min=new_x_min, x_max=new_x_max, 
                            y_min=new_y_min, y_max=new_y_max, 
                            width=128, height=64)
                    display.clear_display()
                    display.graphics(buffer1)
                    print("after plotting", gc.mem_free())


                elif inp_breaker == "nav_r":
                    x_range = eval(form.inp_list()["inp_2"], eval_globals) - eval(form.inp_list()["inp_1"], eval_globals)
                    
                    shift = x_range * 0.2

                    new_x_min = eval(form.inp_list()["inp_1"], eval_globals) + shift
                    new_x_max = eval(form.inp_list()["inp_2"], eval_globals) + shift

                    new_y_min = eval(form.inp_list()["inp_3"], eval_globals)
                    new_y_max = eval(form.inp_list()["inp_4"], eval_globals)

                    form.input_list["inp_1"] = format_number(new_x_min)
                    form.input_list["inp_2"] = format_number(new_x_max)

                    fb1.fill(0)
                    plot_function(fb=fb1, func=polynom1, exp_str=form.inp_list()["inp_0"], 
                            x_min=new_x_min, x_max=new_x_max, 
                            y_min=new_y_min, y_max=new_y_max, 
                            width=128, height=64)
                    display.clear_display()
                    display.graphics(buffer1)
                    print("after plotting", gc.mem_free())

                elif inp_breaker == "back":
                    break

                

            fb1.fill(0)
            form.refresh_rows = (0, form.actual_rows)
            display.clear_display()
            form_refresh.refresh()

        elif inp == "alpha" or inp == "beta":
            keypad_state_manager(x=inp)
            form.update_buffer("")
        elif inp not in ["alpha", "beta", "ok"]:
            form.update_buffer(inp)
        form_refresh.refresh(state=nav.current_state())
    
        time.sleep(0.1)
    print("end of graph", gc.mem_free())

def plot_function(fb, func, exp_str, x_min, x_max, y_min, y_max, width, height):
    # global x_past, y_past
    fb.line(0,31,127,31, 1)
    fb.line(63,0,63,57,1)
    global eval_globals
    x_past=0
    y_past=0
    # Scale factors to map function values to the display's pixel coordinates
    x_scale = (x_max - x_min) /(width)
    y_scale = (y_max - y_min) / (height)


    # # Draw x_min and x_max on the x-axis (adjust positions to avoid overlap)
    # fb.text(str(x_min), 0, 32, 1)          # x_min at the left of x-axis
    # fb.text(str(x_max), 118 - len(str(x_max)) * 8, 32, 1)  # x_max at the right, adjusted for text width

    # # Draw y_min and y_max on the y-axis (adjust positions to avoid overlap)
    # fb.text(str(y_min), 64, 56, 1)         # y_min near the bottom of y-axis
    # fb.text(str(y_max), 64, 0, 1)          # y_max near the top of y-axis

    # Draw labels using the new 3x5 font
    # draw_small_text(fb, "x_min", 0, 33)   # Below x-axis left
    # draw_small_text(fb, "x_max", 108, 33) # Below x-axis right
    # draw_small_text(fb, "y_min", 65, 50)  # Below y-axis bottom
    # draw_small_text(fb, "y_max", 65, 0)   # Above y-axis top
    fb.text("x= ", 0, 56, 1)             # display current x value at which the cursor is placed
    fb.text("y= ", 64, 56, 1)            # display current y value at which the cursor is placed
    
    height -= 8

    # Loop through each x pixel
    for x_pixel in range(width):
        
        # Convert the pixel x-coordinate to the mathematical x-value
        x_value = x_min + (x_pixel) * x_scale

        # Calculate the corresponding y-value for the function
        y_value = func(exp=exp_str,x=x_value)

        # Scale the y-value to the display height and invert it (because displays usually have y=0 at the top)
        y_pixel = int(height - (y_value - y_min) / y_scale)
        
        if func(exp=exp_str,x=x_value)>y_max or func(exp=exp_str,x=x_value)<y_min:

            # print(" pixel= ",x_pixel," ", y_pixel," value= ",x_value," ", y_value ," past= ",x_past," ",y_past)
            x_past=0
            y_past=0
            # fb.vline(x_pixel,y_pixel, 100,1)

        # Ensure y_pixel is within the display range
        if 0 <= y_pixel < height:
            
            fb.pixel(x_pixel-1, y_pixel-1, 1)
            # if x_past!=0 and y_past!=0:
            if x_past*y_past!=0:
                fb.line(x_past, y_past, x_pixel-1, y_pixel-1, 1)
            x_past=x_pixel-1
            y_past=y_pixel-1


def polynom1(exp, x):
    global eval_globals
    # Add 'x' to the dictionary for evaluation
    eval_globals["x"]=x
    # Combine global and local dictionaries
    # context = eval_globals + eval_locals
    # Evaluate the expression
    y = eval(exp, eval_globals)

    return y
