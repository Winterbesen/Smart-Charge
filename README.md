# Smart Charge

This project uses an ESP32 microcontroller to automatically switch a relay on or off depending on electricity prices and CO₂ emissions.

The goal is to use electricity when it is both affordable and environmentally friendly. For example, a charger connected to the relay will only receive power when electricity prices are low and CO₂ emissions are low.

## How it works

The ESP32 retrieves data from two APIs provided by Energi Data Service:

- **DayAheadPrices:** Gets the latest available electricity price for the selected price area (DK2).
- **CO2Emis:** Gets the latest available CO₂ emissions in g/kWh.

The two values are compared with the limits set in the code:

```python
PRICE_AREA = "DK2"

MAX_PRICE = 2.0
MAX_CO2 = 50
```

The relay only turns ON if both conditions are met:

- Electricity price is at or below 2.0 DKK/kWh.
- CO₂ emissions are at or below 50 g/kWh.

If either condition is not met, the relay stays OFF.

The NeoPixel also indicates the status:

- 🟢 **Green:** Electricity is cheap and green, so the relay is ON.
- 🔴 **Red:** Electricity is too expensive, the CO₂ emissions are too high, or there is an API error.

## USB connection and display

The ESP32 is connected to a PC through USB.

The program prints the retrieved electricity prices, CO₂ emissions, green energy status and relay status directly in the serial shell. This makes it possible to follow what the ESP32 is doing and see the API data.

The same information is also displayed on the 20x4 LCD connected to the ESP32.

## Hardware

The following components are used:

- **ESP32** – Runs the program and connects to Wi-Fi.
- **NeoPixel LED (WS2812B)** – Shows the relay status.
- **Relay module** – Controls the power to a connected device, for example a charger.
- **20x4 LCD display** – Displays electricity price, CO₂ emissions, green energy status and relay status.

### Pin connections

| Component | ESP32 GPIO |
|---|---|
| Relay | GPIO 14 |
| NeoPixel | GPIO 26 |
| LCD RS | GPIO 27 |
| LCD Enable | GPIO 25 |
| LCD D4 | GPIO 33 |
| LCD D5 | GPIO 32 |
| LCD D6 | GPIO 21 |
| LCD D7 | GPIO 22 |

## Wi-Fi setup

The project includes a `secrets.py` file where you can enter your own Wi-Fi details.

Open the file and replace the example credentials with your own:

```python
WIFI_SSID = "YOUR_WIFI_NAME"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
```

The project also includes a `boot.py` file, which automatically connects the ESP32 to your Wi-Fi network whenever it starts or reboots.

You just need to enter your Wi-Fi details in `secrets.py` before running the project.

## APIs

Both APIs are publicly available from Energi Data Service:

- [Electricity prices – DayAheadPrices](https://api.energidataservice.dk/dataset/DayAheadPrices)
- [CO₂ emissions – CO2Emis](https://api.energidataservice.dk/dataset/CO2Emis)

The project currently uses DK2 (Eastern Denmark), but the price area can be changed in the code.

All values come from real API responses. No simulated or randomly generated data is used.

## Checking interval

The ESP32 currently checks both APIs every **5 seconds**.

I would recommend increasing this interval, especially if electricity prices fluctuate a lot in your region or country.

Checking too frequently can cause the relay to switch ON and OFF repeatedly when prices move around the set limit. It can also result in API rate limiting if too many requests are made.

Increasing the interval makes the system more stable and reduces unnecessary API requests. You can change the `sleep(5)` value at the bottom of the code to a higher number.

For example:

```python
sleep(300)  # Check every 300 seconds / 5 minutes
```

## Error handling

If an API request fails, gets rate-limited, or returns no data:

- The relay is turned OFF.
- The NeoPixel turns red.
- The LCD displays an error message.
- The error is also printed in the serial shell.
- The program tries again after the checking interval.

The system never uses fake data as a fallback.

## Getting started

1. Install MicroPython on your ESP32.
2. Connect the components using the pin connections above.
3. Connect the ESP32 to your PC using USB.
4. Upload the project files to your ESP32.
5. Enter your Wi-Fi name and password in `secrets.py`.
6. Adjust the maximum electricity price, CO₂ limit and checking interval if needed.
7. Restart the ESP32.

The program will automatically connect to Wi-Fi and start checking the APIs.

---

**Note:** If you use the relay to control a mains-powered charger or other device, make sure the relay is properly rated and that all mains wiring is safely enclosed and insulated.

<img width="415" height="142" alt="usingrealapidata" src="https://github.com/user-attachments/assets/d3870c8a-5b68-4759-9426-880ff8d052b9" />

