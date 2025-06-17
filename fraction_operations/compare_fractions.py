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
        append_to_form("Error: Denominator cannot be zero")
        return num, denom
    if denom < 0:  # Ensure denominator is positive
        num, denom = -num, -denom
    if num == 0:
        return 0, 1
    g = gcd(abs(num), abs(denom))
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
    # Find the last space before 21 characters
    split_idx = text[:21].rfind(' ')
    if split_idx == -1:  # No space found, split at 21
        split_idx = 21
    form.form_list.append(text[:split_idx])
    # Recursively handle the remaining text
    remaining = text[split_idx:].strip()
    if remaining:
        append_to_form(remaining)

def compare_fractions_calculator(fractions):
    """Find the smallest and largest fractions."""
    if not fractions:
        append_to_form("Error: No valid fractions to compare")
        return None, None
    # Convert fractions to a common denominator for comparison
    denom_product = 1
    for _, denom in fractions:
        denom_product *= denom
    # Scale numerators by product of other denominators
    scaled_nums = []
    for num, denom in fractions:
        factor = denom_product // denom
        scaled_nums.append(num * factor)
    # Find indices of min and max
    min_idx = scaled_nums.index(min(scaled_nums))
    max_idx = scaled_nums.index(max(scaled_nums))
    return fractions[min_idx], fractions[max_idx]

def compare_fractions(db={}):
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
            # Clear any fields beyond the first two
            if len(form.form_list) > 2:
                form.form_list = form.form_list[:2]
            
            data = form.input_list["inp_0"].split("+")
            fractions = parse_input(data)
            
            smallest, largest = compare_fractions_calculator(fractions)
            if smallest is None or largest is None:
                append_to_form("Smallest: None")
                append_to_form("Largest: None")
            else:
                append_to_form(f"Smallest: {fraction_to_string(*smallest)}")
                append_to_form(f"Largest: {fraction_to_string(*largest)}")

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