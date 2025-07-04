import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def gcd_computer(a, b):
    """Calculate the Greatest Common Divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(num, denom):
    """Simplify a fraction by dividing numerator and denominator by their GCD."""
    if denom == 0:
        append_to_form("Error: Denominator cannot be zero")
        return num, denom
    if denom < 0:  # Ensure denominator is positive
        num, denom = -num, -denom
    if num == 0:
        return 0, 1
    g = gcd_computer(abs(num), abs(denom))
    return num // g, denom // g

def parse_fraction(frac_str):
    """Parse a fraction string like 'a/b' or 'a' into (numerator, denominator)."""
    try:
        if '/' not in frac_str:
            return int(frac_str.strip()), 1
        num_str, denom_str = frac_str.split('/')
        num = int(num_str.strip())
        denom = int(denom_str.strip())
        return simplify_fraction(num, denom)
    except ValueError:
        append_to_form(f"Error: Invalid fraction: {frac_str}")
        return None

def parse_power(power_str):
    """Parse a power string into an integer."""
    try:
        return int(power_str.strip())
    except ValueError:
        append_to_form(f"Error: Invalid power: {power_str}")
        return None

def fraction_to_string(num, denom):
    """Convert a fraction to string format."""
    if denom == 1:
        return str(num)
    return f"{num}/{denom}"

def append_to_form(text):
    """Append text to form.form_list, splitting at 21 characters at word boundaries."""
    if len(text) <= 21:
        form.form_list.append(text)
        return
    split_idx = text[:21].rfind(' ')
    if split_idx == -1:
        split_idx = 21
    form.form_list.append(text[:split_idx])
    remaining = text[split_idx:].strip()
    if remaining:
        append_to_form(remaining)

def power_fraction_calculator(num, denom, power):
    """Raise a fraction (num/denom) to the given power."""
    if denom == 0:
        append_to_form("Error: Denominator=0")
        return None
    if num == 0 and power <= 0:
        append_to_form("Error: 0^non-positive power")
        return None
    if power == 0:
        return 1, 1  # Any non-zero fraction to power 0 is 1/1
    # Handle negative power by inverting the fraction
    if power < 0:
        num, denom = denom, num  # Invert fraction
        power = -power
        if num == 0:
            append_to_form("Error: 0^negative power")
            return None
    # Compute num^power / denom^power
    result_num = pow(num, power)
    result_denom = pow(denom, power)
    return simplify_fraction(result_num, result_denom)

def power_fraction(db={}):
    form.input_list = {"inp_0": "3/4", "inp_1": "2"}
    form.form_list = ["Enter fraction:", "inp_0", "Enter power:", "inp_1"]
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
            if len(form.form_list) > 4:
                form.form_list = form.form_list[:4]
            
            fraction_str = form.input_list.get("inp_0", "")
            power_str = form.input_list.get("inp_1", "")
            
            fraction = parse_fraction(fraction_str)
            power = parse_power(power_str)
            
            append_to_form("Result:")
            if fraction is None or power is None:
                append_to_form("None")
            else:
                num, denom = fraction
                result = power_fraction_calculator(num, denom, power)
                if result is None:
                    append_to_form("None")
                else:
                    result_num, result_denom = result
                    append_to_form(fraction_to_string(result_num, result_denom))
            
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