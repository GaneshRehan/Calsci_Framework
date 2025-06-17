from data_modules.object_handler import display, form, form_refresh
form.form_list = ["CalSciCalSciCalSciCal", "alSciCalSciCalSciCalS", "lSciCalSciCalSciCalSc", "SciCalSciCalSciCalSci", "ciCalSciCalSciCalSciC", "iCalSciCalSciCalSciCa", "CalSciCalSciCalSciCal", "alSciCalSciCalSciCalS"]
form.update()
# display.clear_display()
form_refresh.refresh()



from data_modules.app_handler import app_handler
from process_modules.auto_wifi_connector import auto_wifi_connector
import json

boot_up_file = "database/boot_up.json"
with open(boot_up_file, 'r') as file:
        boot_up_data = json.load(file)

print(boot_up_data)

if boot_up_data["states"]["wifi_connected"]:
    auto_wifi_connector()

if boot_up_data["states"]["dark_mode"]:
      from settings.dark_mode import toggle_display_mode
      toggle_display_mode()

if boot_up_data["states"]["backlight"]:
      from settings.backlight import backlight
      backlight()

app_handler(last_used_app=boot_up_data["data_points"]["last_used_app"], last_used_app_folder=boot_up_data["data_points"]["last_used_app_folder"])


