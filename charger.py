
from machine import Pin
from time import sleep
from neopixel import NeoPixel

try:
    import requests
except ImportError:
    import urequests as requests

from gpio_lcd import GpioLcd


relay = Pin(14, Pin.OUT)

n = 12
p = 26
np = NeoPixel(Pin(p, Pin.OUT), n)

lcd = GpioLcd(
    rs_pin=Pin(27),
    enable_pin=Pin(25),
    d4_pin=Pin(33),
    d5_pin=Pin(32),
    d6_pin=Pin(21),
    d7_pin=Pin(22),
    num_lines=4,
    num_columns=20
)


PRICE_AREA = "DK2"

MAX_PRICE = 2.0
MAX_CO2 = 50


elpris_url = (
    "https://api.energidataservice.dk/dataset/"
    "DayAheadPrices?"
    "start=StartOfDay&end=now&"
    "filter=%7B%22PriceArea%22%3A%5B%22"
    + PRICE_AREA +
    "%22%5D%7D&"
    "sort=TimeUTC%20desc&limit=1"
)

co2_url = (
    "https://api.energidataservice.dk/dataset/"
    "CO2Emis?"
    "start=now&startOffset=-PT15M&"
    "filter=%7B%22PriceArea%22%3A%5B%22"
    + PRICE_AREA +
    "%22%5D%7D&"
    "sort=Minutes5UTC%20desc&limit=1"
)


def get_api_data(url):

    response = requests.get(url)

    status_code = response.status_code

    if status_code == 429:
        response.close()
        raise Exception("API RATE LIMITED")

    if status_code != 200:
        response.close()
        raise Exception("HTTP ERROR: " + str(status_code))

    try:
        data = response.json()
    finally:
        response.close()

    return data


while True:

    try:

        print("Fetching real API data...")

        # Get real electricity price
        price_json = get_api_data(elpris_url)

        # Get real CO2 data
        co2_json = get_api_data(co2_url)

        price_records = price_json["records"]
        co2_records = co2_json["records"]

        if not price_records or not co2_records:
            raise Exception("API returned no records")

        # Real electricity price (DKK/kWh)
        x = (
            price_records[0]["DayAheadPriceDKK"]
            / 1000
        )

        # Real CO2 emission
        co2 = co2_records[0]["CO2Emission"]

        # Determine whether energy is green
        groen_energi = co2 <= MAX_CO2

        print("Using REAL API data!")

        # Control relay
        if x <= MAX_PRICE and groen_energi:

            relay.value(1)
            status = "ON"
            np[0] = (0, 10, 0)

        else:

            relay.value(0)
            status = "OFF"
            np[0] = (10, 0, 0)

        np.write()

        # Print real data
        print("----------------------")
        print("Electricity price:", x, "DKK/kWh")
        print("CO2:", co2, "g/kWh")
        print("Green energy:", groen_energi)
        print("Relay:", status)
        print("----------------------")

        # Update LCD
        lcd.clear()

        lcd.move_to(0, 0)
        lcd.putstr(
            "Elpris: {:.3f} DKK".format(x)
        )

        lcd.move_to(0, 1)
        lcd.putstr(
            "CO2: {:.1f} g/kWh".format(co2)
        )

        lcd.move_to(0, 2)
        lcd.putstr(
            "Groen energi: {}".format(
                "JA" if groen_energi else "NEJ"
            )
        )

        lcd.move_to(0, 3)
        lcd.putstr(
            "Relay: {}".format(status)
        )

    except Exception as e:

        print("API ERROR:", e)

        # Always turn relay OFF if API fails
        relay.value(0)

        # Red LED indicates error
        np[0] = (10, 0, 0)
        np.write()

        lcd.clear()

        lcd.move_to(0, 0)

        if str(e) == "API RATE LIMITED":
            lcd.putstr("API RATE LIMITED")
        else:
            lcd.putstr("API ERROR")

        lcd.move_to(0, 1)
        lcd.putstr(str(e)[:20])

        lcd.move_to(0, 2)
        lcd.putstr("Relay: OFF")

    sleep(5)
