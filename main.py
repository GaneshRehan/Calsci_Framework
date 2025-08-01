from data_modules.object_handler import display, form, form_refresh
from data_modules.app_handler import app_handler
import json

form.form_list = [
    "CalSciCalSciCalSciCal", "alSciCalSciCalSciCalS", "lSciCalSciCalSciCalSc",
    "SciCalSciCalSciCalSci", "ciCalSciCalSciCalSciC", "iCalSciCalSciCalSciCa",
    "CalSciCalSciCalSciCal", "alSciCalSciCalSciCalS"
]
form.update()
form_refresh.refresh()

# Load boot-up configuration
boot_up_file = "database/boot_up.json"
try:
    with open(boot_up_file, 'r') as file:
        boot_up_data = json.load(file)
except Exception as e:
    print("Error loading boot config:", e)
    boot_up_data = {
        "states": {"dark_mode": False, "backlight": True},
        "data_points": {"last_used_app": "default", "last_used_app_folder": "apps"}
    }

# Handle optional boot-up states
# if boot_up_data["states"].get("dark_mode"):
#     from settings.dark_mode import toggle_display_mode
#     toggle_display_mode()

# if boot_up_data["states"].get("backlight"):
#     from settings.backlight import backlight
#     backlight()

# Launch last used app
app_handler(
    last_used_app=boot_up_data["data_points"].get("last_used_app", "default"),
    last_used_app_folder=boot_up_data["data_points"].get("last_used_app_folder", "apps")
)
