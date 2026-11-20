import network
import secrets
import requests
from machine import reset
from time import ticks_ms

ssid = secrets.SSID
password = secrets.PASSWORD

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not wlan.isconnected():
    print("Connecting to WiFi...")
    wlan.connect(ssid, password)

    start = ticks_ms()
    while not wlan.isconnected():
        if ticks_ms() - start > 10000:
            print("WiFi connection failed!")
            reset()

print("Connected to", ssid)

print("Checking internet connection...")

try:
    res = requests.get("https://google.com/")

    if res.status_code == 200:
        print("Internet connection successful!")
    else:
        print("Internet check failed:", res.status_code)

    res.close()

except Exception as e:
    print("No internet connection:", e)