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

def parse_input(input_list):
    """Parse a list of fraction strings like ['a/b', 'c/d', 'e/f']."""
    if not input_list:
        append_to_form("Error: No fractions provided")
        return []
    fractions = []
    for f in input_list:
        result = parse_fraction(f)
        if result is not None:
            fractions.append(result)
    return fractions

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

def compute_gcd(num, denom):
    """Calculate the GCD of a numerator and denominator."""
    if denom == 0:
        return "Error: Denom=0"
    return str(gcd_computer(abs(num), abs(denom)))

def gcd_for_fractions(fractions):
    """Calculate GCD of all numerators and all denominators together."""
    if not fractions:
        append_to_form("No valid fractions")
        return
    numerators = [num for num, _ in fractions]
    denominators = [denom for _, denom in fractions]
    
    # Check for zero denominators
    if 0 in denominators:
        append_to_form("Error: Denom=0")
        return
    
    # Compute GCD of all numerators
    num_gcd = abs(numerators[0]) if numerators else 0
    for num in numerators[1:]:
        num_gcd = gcd_computer(num_gcd, abs(num))
    
    # Compute GCD of all denominators
    denom_gcd = denominators[0] if denominators else 1
    for denom in denominators[1:]:
        denom_gcd = gcd_computer(denom_gcd, abs(denom))
    
    # Compute final GCD of the numerator GCD and denominator GCD
    final_gcd = gcd_computer(num_gcd, denom_gcd)
    append_to_form(f"GCD: {final_gcd}")

def gcd(db={}):
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
            if len(form.form_list) > 2:
                form.form_list = form.form_list[:2]
            
            data = form.input_list["inp_0"].split("+")
            fractions = parse_input(data)
            
            gcd_for_fractions(fractions)
            
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