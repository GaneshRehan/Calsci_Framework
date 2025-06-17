import os
import json
from data_modules.object_handler import data_bucket, current_app
from settings.dark_mode import display_mode_label
from settings.backlight import backlight_label

def main():
    boot_up_file = "database/boot_up.json"

    with open(boot_up_file, 'r') as file:
        boot_up_data = json.load(file)

    if data_bucket["connection_status_g"]:
        boot_up_data["states"]["wifi_connected"] = True

    boot_up_data["data_points"]["last_used_app"] = current_app[0] if current_app[0] != "update" else "home"
    boot_up_data["data_points"]["last_used_app_folder"] = current_app[1] if current_app[1] != "update" else "application_modules"
    boot_up_data["states"]["dark_mode"] = display_mode_label == "dark_mode"
    boot_up_data["states"]["backlight"] = backlight_label == "backlight off"
    print(f"display_mode_label{display_mode_label}")
    print(f"dount {display_mode_label == "dark_mode"}")


    print("before shutting")
    print(boot_up_data)

    with open(boot_up_file, 'w') as file:
        json.dump(boot_up_data, file)

