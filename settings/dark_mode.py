from machine import Pin # type: ignore
from data_modules.object_handler import display

# Initialize display mode state
display_mode_label = "dark_mode"  # Assume light mode by default
_is_inverted = 0  # 0 for light mode, 1 for dark mode
display.invert(_is_inverted)  # Set initial state

def toggle_display_mode(db={}):
    global display_mode_label, _is_inverted
    if _is_inverted == 1:  # If in dark mode
        display.invert(0)  # Switch to light mode
        _is_inverted = 0
        display_mode_label = "dark_mode"
        print("display mode lable is")
        print(display_mode_label)
        return "dark_mode"
    else:  # If in light mode
        display.invert(1)  # Switch to dark mode
        _is_inverted = 1
        display_mode_label = "light_mode"
        print("display mode lable is")
        print(display_mode_label)
        return "light_mode"
    