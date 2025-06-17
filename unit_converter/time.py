import utime  # type:ignore
from math import *
import machine
from data_modules.object_handler import display, nav, typer, keypad_state_manager, form, form_refresh, keymap
from process_modules import boot_up_data_update
from data_modules.object_handler import current_app

def append_to_form(text):
    """Append text to form.form_list, splitting at 21 characters at word boundaries."""
    try:
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
    except Exception as e:
        # print(f"append_to_form error: {e}")  # Debug
        form.form_list.append("Error: Display")

def parse_value_and_unit(input_str):
    """Parse a string like '5h' into a float value and unit."""
    try:
        input_str = input_str.strip()
        # print(f"Parsing input: {input_str}")  # Debug
        if not input_str:
            append_to_form("Error: Empty input")
            return None, None
        
        # Find the boundary between value and unit
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
        
        value = float(value_str)
        # print(f"Parsed: value={value}, unit={unit}")  # Debug
        return value, unit
    except Exception as e:
        # print(f"parse_value_and_unit error: {e}")  # Debug
        append_to_form("Error: Parse failed")
        return None, None

def convert_time(value, source_unit, target_unit):
    """Convert time from source unit to target unit via seconds."""
    try:
        conversion_factors = {
            's': 1.0,              # seconds
            'min': 1.0/60,         # minutes
            'h': 1.0/3600,         # hours
            'd': 1.0/(24*3600),    # days
            'wk': 1.0/(7*24*3600), # weeks
            'ms': 1000.0           # milliseconds
        }
        
        source_unit = source_unit.lower()
        target_unit = target_unit.strip().lower()
        
        if source_unit not in conversion_factors:
            append_to_form(f"Error: Invalid source unit: {source_unit}")
            return None
        if target_unit not in conversion_factors:
            append_to_form(f"Error: Invalid target unit: {target_unit}")
            return None
        
        # Convert source unit to seconds (divide by factor since factors are seconds to unit)
        value_in_seconds = value / conversion_factors[source_unit]
        # Convert seconds to target unit (multiply by factor)
        converted_value = value_in_seconds * conversion_factors[target_unit]
        # Round to 4 decimal places for readability
        return round(converted_value, 4)
    except Exception as e:
        # print(f"convert_time error: {e}")  # Debug
        append_to_form("Error: Conversion failed")
        return None

def time(db={}):
    try:
        # print("Initializing time_converter")  # Debug
        form.input_list = {"inp_0": "5h", "inp_1": "min"}
        form.form_list = ["Enter time:", "inp_0", "To unit:", "inp_1"]
        form.update()
        display.clear_display()
        form_refresh.refresh()
    except Exception as e:
        # print(f"Initialization error: {e}")  # Debug
        form.form_list = ["Error: Init failed"]
        form.update()
        display.clear_display()
        form_refresh.refresh()

    while True:
        try:
            # print("Main loop iteration")  # Debug
            inp = typer.start_typing()
            # print(f"Input received: {inp}")  # Debug
            if inp == "back":
                current_app[0] = "unit_converter"
                current_app[1] = "scientific_calculator"
                break

            if inp == "ok":
                if len(form.form_list) > 4:
                    form.form_list = form.form_list[:4]
                
                input_str = form.input_list.get("inp_0", "")
                target_unit = form.input_list.get("inp_1", "")
                # print(f"Processing: inp_0={input_str}, inp_1={target_unit}")  # Debug
                
                value, source_unit = parse_value_and_unit(input_str)
                
                append_to_form("Result:")
                if value is None or source_unit is None:
                    append_to_form("None")
                else:
                    result = convert_time(value, source_unit, target_unit)
                    if result is None:
                        append_to_form("None")
                    else:
                        append_to_form(f"{str(result)}{form.input_list['inp_1']}")
                
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
            utime.sleep(0.15)
        except Exception as e:
            # print(f"Main loop error: {e}")  # Debug
            append_to_form("Error: Loop failed")
            form.update()
            display.clear_display()
            form_refresh.refresh()
            utime.sleep(0.15)