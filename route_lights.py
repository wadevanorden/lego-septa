import time

from gpiozero import LED

from mappings import STOPS_TO_PINS, ROUTES

LEDS = {stop: LED(pin) for stop, pin in STOPS_TO_PINS.items()}

ROUTE_NAMES = {
    "AIR": "Airport",
    "CHE": "Chestnut Hill East",
    "CHW": "Chestnut Hill West",
    "CYN": "Cynwyd",
    "FOX": "Fox Chase",
    "GLN": "Lansdale/Doylestown (Local)",
    "LAN": "Lansdale/Doylestown (Express)",
    "MED": "Media/Wawa",
    "NOR": "Norristown",
    "PAO": "Paoli/Thorndale",
    "TRE": "Trenton",
    "WAR": "Warminster",
    "WIL": "Wilmington/Newark",
    "WTR": "West Trenton",
}

# Stops ordered from 30th Street outward along each route, based on the map
ROUTE_STOP_ORDER = {
    "AIR": ["30th", "Suburban Station", "Jefferson Station", "Airport"],
    "CHE": ["30th", "Suburban Station", "Jefferson Station", "Wayne Junction", "Chestnut Hill East"],
    "CHW": ["30th", "Suburban Station", "Jefferson Station", "North Broad", "Chestnut Hill West"],
    "CYN": ["30th", "Suburban Station", "Cynwyd"],
    "FOX": ["30th", "Suburban Station", "Jefferson Station", "Wayne Junction", "Fox Chase"],
    "GLN": ["30th", "Suburban Station", "Jefferson Station", "North Broad", "Wayne Junction", "Glenside", "West Trenton", "Lansdale", "Doylestown"],
    "LAN": ["30th", "Suburban Station", "Jefferson Station", "North Broad", "North Philadelphia", "Wayne Junction", "Glenside", "Lansdale", "Doylestown"],
    "MED": ["30th", "Suburban Station", "Jefferson Station", "Wawa"],
    "NOR": ["30th", "Suburban Station", "Jefferson Station", "North Broad", "Norristown"],
    "PAO": ["30th", "Bryn Mawr", "Paoli", "Malvern", "Thorndale"],
    "TRE": ["30th", "Suburban Station", "Jefferson Station", "North Philadelphia", "Trenton"],
    "WAR": ["30th", "Suburban Station", "Jefferson Station", "Wayne Junction", "Glenside", "Warminster"],
    "WIL": ["30th", "Suburban Station", "Jefferson Station", "Marcus Hook", "Wilmington", "Newark DE"],
    "WTR": ["30th", "Suburban Station", "Jefferson Station", "West Trenton"],
}

def all_off():
    for led in LEDS.values():
        led.off()

def display_route(route, step_delay=0.4, hold=1.5):
    stops = ROUTE_STOP_ORDER[route]
    name = ROUTE_NAMES.get(route, route)
    print(f"Route: {name} ({route}) — {len(stops)} stops")

    # Light up stops one at a time from 30th outward
    for stop in stops:
        LEDS[stop].on()
        time.sleep(step_delay)

    # Hold all on
    time.sleep(hold)

    # Turn them off retreating back toward 30th
    for stop in reversed(stops):
        LEDS[stop].off()
        time.sleep(step_delay / 2)

    time.sleep(0.3)

def main():
    try:
        print("Starting route display...")
        while True:
            for route in ROUTES:
                display_route(route, step_delay=0.4, hold=1.5)
            print("All routes complete, restarting...\n")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
        all_off()

if __name__ == "__main__":
    main()
