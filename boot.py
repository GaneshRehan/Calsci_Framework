import gc
import time
import network
import json

# Enable garbage collector
gc.enable()
gc.collect()
print("free ram initially =", gc.mem_free())
print("ram allocated initially =", gc.mem_alloc())

# Deinitialize and reinitialize WiFi cleanly
sta_if = network.WLAN(network.STA_IF)
sta_if.active(False)
time.sleep(0.5)
gc.collect()
sta_if.active(True)

# Attempt WiFi connection using /database/wifi.json
wifi_config_file = "/database/wifi.json"

try:
    with open(wifi_config_file, "r") as f:
        wifi_data = json.load(f)
        
    with open("/database/boot_up.json") as f:
        boot_data = json.load(f)
        
    if boot_data["states"].get("wifi_connected"):

        scanned = sta_if.scan()
        available_ssids = [net[0].decode() for net in scanned]

        for entry in wifi_data:
            ssid = entry.get("ssid")
            password = entry.get("password")
            if ssid in available_ssids:
                print("Connecting to:", ssid)
                sta_if.connect(ssid, password)
                for _ in range(100):
                    if sta_if.isconnected():
                        break
                    time.sleep(0.1)
                break

        print("WiFi connected:", sta_if.isconnected())
        if sta_if.isconnected():
            print("IP config:", sta_if.ifconfig())

except Exception as e:
    print("WiFi setup skipped or failed:", e)

# from settings.backlight import backlight_pin
# backlight_pin.off()  # Save power or show clean black screen
