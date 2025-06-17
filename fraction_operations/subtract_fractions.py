import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def gcd(a, b):
    """Calculate the Greatest Common Divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(num, denom):
    """Simplify a fraction by dividing numerator and denominator by their GCD."""
    if denom == 0:
        raise ValueError("Denominator cannot be zero")
    if denom < 0:  # Ensure denominator is positive
        num, denom = -num, -denom
    if num == 0:
        return 0, 1
    g = gcd(abs(num), abs(denom))
    return num // g, denom // g

def parse_fraction(frac_str):
    """Parse a fraction string like 'a/b' or 'a' into (numerator, denominator)."""
    if '/' not in frac_str:
        return int(frac_str.strip()), 1
    num_str, denom_str = frac_str.split('/')
    num = int(num_str.strip())
    denom = int(denom_str.strip())
    return simplify_fraction(num, denom)

def parse_input(input_list):
    """Parse a list of fraction strings like ['a/b', 'c/d', 'e/f']."""
    if not input_list:
        raise ValueError("No fractions provided")
    return [parse_fraction(f) for f in input_list]

def fraction_to_string(num, denom):
    """Convert a fraction to string format."""
    if denom == 1:
        return str(num)
    return f"{num}/{denom}"

def subtract_fractions_calculator(fractions):
    """Subtract fractions in sequence: (a/b) - (c/d) - ..."""
    if not fractions:
        return 0, 1
    num, denom = fractions[0]
    for num2, denom2 in fractions[1:]:
        num = num * denom2 - num2 * denom
        denom = denom * denom2
        num, denom = simplify_fraction(num, denom)
    return num, denom

def subtract_fractions(db={}):
    form.input_list = {"inp_0": "1/2+2/3+3/4+5/6"}
    form.form_list = ["Enter fractions:", "inp_0"]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0] = "fraction_operations"
            current_app[1] = "scientific_calculator"
            break

        if inp == "ok":
            data = form.input_list["inp_0"].split("+")
            fractions = parse_input(data)
            
            result = subtract_fractions_calculator(fractions)
            if len(form.form_list) == 2:
                form.form_list.append("Difference is:")
                form.form_list.append(fraction_to_string(*result))
            else:
                form.form_list[-2] = "Difference is:"
                form.form_list[-1] = fraction_to_string(*result)

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