import utime as time  # type:ignore
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
    """Parse a string like '5kg' into a float value and unit."""
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

def convert_mass(value, source_unit, target_unit):
    """Convert mass from source unit to target unit via kilograms."""
    try:
        # Conversion factors: multiply to convert from kg to target unit
        conversion_factors = {
    # --- SI & Metric System ---
    'kg': 1.0,                   # kilograms (SI base unit)
    'g': 1000.0,                 # grams
    'mg': 1_000_000.0,           # milligrams
    'µg': 1_000_000_000.0,       # micrograms
    'ng': 1_000_000_000_000.0,   # nanograms
    't': 0.001,                  # metric tons (tonnes)
    'kt': 1e-6,                  # kilotonnes
    'Mt': 1e-9,                  # megatonnes (nuclear yields)

    # --- US Customary & Imperial ---
    'lb': 2.2046226218,          # pounds (avoirdupois)
    'oz': 35.27396195,           # ounces (avoirdupois)
    'st': 0.1574730444,          # stones (14 lb)
    'ton_us': 0.001102311311,    # US short tons (2000 lb)
    'ton_uk': 0.0009842065276,   # UK long tons (2240 lb)
    'gr': 15432.35835,           # grains (1/7000 lb)

    # --- Troy & Precious Metals ---
    'oz_t': 32.1507466,          # troy ounces (31.1035 g)
    'lb_t': 2.67922888,          # troy pounds (12 oz_t)
    'dwt': 643.014931,           # pennyweight (24 gr)

    # --- Asian Units ---
    'jin': 2.0,                  # Chinese catty (~500g)
    'liang': 20.0,               # Chinese taels (~50g)
    'kan': 0.2666666667,         # Japanese kan (3.75 kg)

    # --- Physics & Astronomy ---
    'u': 6.02214076e26,          # atomic mass units (1 Da ≈ 1.66e-27 kg)
    'M⊕': 3.003e-7,              # Earth masses (5.972e24 kg)
    'M☉': 5.027e-31,             # Solar masses (1.989e30 kg)

    # --- Historical & Obsolete ---
    'slug': 0.0685217656,        # Imperial slug (14.5939 kg)
    'hyl': 0.101971621,           # Metric technical mass unit (9.80665 kg)
    'carat': 5000.0              # Metric carats (200 mg)
}
        
        source_unit = source_unit.lower()
        target_unit = target_unit.strip().lower()
        
        if source_unit not in conversion_factors:
            append_to_form(f"Error: Invalid source unit: {source_unit}")
            return None
        if target_unit not in conversion_factors:
            append_to_form(f"Error: Invalid target unit: {target_unit}")
            return None
        
        # Convert source unit to kilograms (divide by factor)
        value_in_kg = value / conversion_factors[source_unit]
        # Convert kilograms to target unit (multiply by factor)
        result = value_in_kg * conversion_factors[target_unit]
        
        # Round to 4 decimal places for readability
        return round(result, 4)
    except Exception as e:
        # print(f"convert_mass error: {e}")  # Debug
        append_to_form("Error: Conversion failed")
        return None

def mass(db={}):
    try:
        # print("Initializing mass")  # Debug
        form.input_list = {"inp_0": "5kg", "inp_1": "g"}
        form.form_list = ["Enter mass:", "inp_0", "To unit:", "inp_1"]
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
                    result = convert_mass(value, source_unit, target_unit)
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
            time.sleep(0.15)
        except Exception as e:
            # print(f"Main loop error: {e}")  # Debug
            append_to_form("Error: Loop failed")
            form.update()
            display.clear_display()
            form_refresh.refresh()
            time.sleep(0.15)