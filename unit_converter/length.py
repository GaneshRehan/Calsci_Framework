import utime as time  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

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

def parse_value_and_unit(input_str):
    """Parse a string like '5m' into a float value and unit."""
    input_str = input_str.strip()
    if not input_str:
        append_to_form("Error: Empty input")
        return None, None
    
    value_str = ''
    unit = ''
    i = 0
    while i < len(input_str):
        if input_str[i].isdigit() or input_str[i] in '.+-':
            value_str += input_str[i]
            i += 1
        else:
            unit = input_str[i:].strip().lower()
            break
    else:
        value_str = input_str.strip()
    
    if not value_str:
        append_to_form(f"Error: No value in: {input_str}")
        return None, None
    if not unit:
        append_to_form(f"Error: No unit in: {input_str}")
        return None, None
    
    try:
        value = float(value_str)
        return value, unit
    except ValueError:
        append_to_form(f"Error: Invalid value: {value_str}")
        return None, None

def convert_length(value, source_unit, target_unit):
    """Convert length from source unit to target unit via meters."""
    conversion_factors = {
        'm': 1.0,               # meters (SI base unit)
        'km': 0.001,            # kilometers
        'cm': 100.0,            # centimeters
        'mm': 1000.0,           # millimeters
        'µm': 1_000_000.0,      # micrometers
        'nm': 1_000_000_000.0,  # nanometers
        'dam': 0.1,             # decameters
        'hm': 0.01,             # hectometers
        'in': 39.37007874,      # inches
        'ft': 3.280839895,      # feet
        'yd': 1.093613298,      # yards
        'mi': 0.000621371192,   # miles
        'nmi': 0.000539956803,  # nautical miles
        'furlong': 0.00497096954, # furlongs
        'league': 0.00020712373, # leagues
        'AU': 6.68458712e-12,   # astronomical units
        'ly': 1.05700083e-16,   # light-years
        'pc': 3.24077929e-17,   # parsecs
        'mil': 39370.07874,     # mils
        'fathom': 0.546806649,  # fathoms
        'rod': 0.1988387815,    # rods
        'chain': 0.0497096954,  # chains
        'point': 2834.64567,    # points
        'pica': 236.220472,     # picas
    }
    
    source_unit = source_unit.lower()
    target_unit = target_unit.strip().lower()
    
    if source_unit not in conversion_factors:
        append_to_form(f"Error: Invalid source unit: {source_unit}")
        return None
    if target_unit not in conversion_factors:
        append_to_form(f"Error: Invalid target unit: {target_unit}")
        return None
    
    value_in_meters = value / conversion_factors[source_unit]
    converted_value = value_in_meters * conversion_factors[target_unit]
    return converted_value

def length(db={}):
    """Length conversion function with two checkboxes for precision control."""
    form.input_list = {
        "inp_0": "10km",
        "inp_1": "m",
        "chk_0": False,  # Full precision (6 decimals)
        "chk_1": False   # Half precision (3 decimals)
    }
    form.form_list = [
        "Enter length:",
        "inp_0",
        "To unit:",
        "inp_1",
        "[ ] Full precision",
        "[ ] Half precision"
    ]
    form.update()
    display.clear_display()
    form_refresh.refresh()

    while True:
        inp = typer.start_typing()
        if inp == "back":
            current_app[0] = "unit_converter"
            current_app[1] = "scientific_calculator"
            break

        if inp == "ok":
            current_field = form.form_list[form.menu_cursor]
            checkbox_labels = ["Full precision", "Half precision"]
            if any(label in current_field for label in checkbox_labels):
                # Determine which checkbox was toggled
                checkbox_index = next(i for i, label in enumerate(checkbox_labels) if label in current_field)
                checkbox_key = f"chk_{checkbox_index}"
                
                # Toggle the selected checkbox
                new_state = not form.input_list[checkbox_key]
                form.input_list[checkbox_key] = new_state
                
                # Reset other checkbox if toggling to True
                if new_state:
                    other_index = 1 - checkbox_index  # 0 if index is 1, 1 if index is 0
                    form.input_list[f"chk_{other_index}"] = False
                    form.form_list[4 + other_index] = f"[ ] {checkbox_labels[other_index]}"
                
                # Update the selected checkbox label
                form.form_list[4 + checkbox_index] = f"[{'X' if new_state else ' '}] {checkbox_labels[checkbox_index]}"
                
                form.refresh_rows = (4 - form.menu_display_position, 6 - form.menu_display_position)
                form.display_buffer = form.form_list[form.menu_display_position:form.menu_display_position+form.menu_display_size]
                form.display_cursor = form.menu_cursor - form.menu_display_position
                form_refresh.refresh()

        if inp == "exe":
            if len(form.form_list) > 6:
                form.form_list = form.form_list[:6]
            
            input_str = form.input_list.get("inp_0", " ")
            target_unit = form.input_list.get("inp_1", " ")
            precision_mode = 0  # Default to integer
            if form.input_list.get("chk_0", False):
                precision_mode = 6  # Full precision
            elif form.input_list.get("chk_1", False):
                precision_mode = 3  # Half precision
            
            value, source_unit = parse_value_and_unit(input_str)
            
            append_to_form("Result:")
            if value is None or source_unit is None:
                append_to_form("None")
            else:
                result = convert_length(value, source_unit, target_unit)
                if result is None:
                    append_to_form("None")
                else:
                    result_str = f"{result:.{precision_mode}f}{target_unit}"
                    if precision_mode == 0:
                        result_str = f"{round(result)}{target_unit}"
                    append_to_form(result_str)
            
            form.update()
            display.clear_display()
            form_refresh.refresh()
            
        if inp == "alpha" or inp == "beta":
            keypad_state_manager(x=inp)
            form.update_buffer("")

        if inp == "off":
            boot_up_data_update.main()
            machine.deepsleep()
        
        if inp not in ["alpha", "beta", "ok", "ans"]:
            form.update_buffer(inp)
        
        form_refresh.refresh(state=nav.current_state())
        time.sleep(0.15)

