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

# Stops ordered from terminus inward toward 30th Street
ROUTE_STOP_ORDER = {
    "AIR": ["Airport", "Jefferson Station", "Suburban Station", "30th"],
    "CHE": ["Chestnut Hill East", "Wayne Junction", "Jefferson Station", "Suburban Station", "30th"],
    "CHW": ["Chestnut Hill West", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    "CYN": ["Cynwyd", "Suburban Station", "30th"],
    "FOX": ["Fox Chase", "Wayne Junction", "Jefferson Station", "Suburban Station", "30th"],
    "GLN": ["Doylestown", "Lansdale", "West Trenton", "Glenside", "Wayne Junction", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    "LAN": ["Doylestown", "Lansdale", "Glenside", "Wayne Junction", "North Philadelphia", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    "MED": ["Wawa", "Jefferson Station", "Suburban Station", "30th"],
    "NOR": ["Norristown", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    "PAO": ["Thorndale", "Malvern", "Paoli", "Bryn Mawr", "30th"],
    "TRE": ["Trenton", "North Philadelphia", "Jefferson Station", "Suburban Station", "30th"],
    "WAR": ["Warminster", "Glenside", "Wayne Junction", "Jefferson Station", "Suburban Station", "30th"],
    "WIL": ["Newark DE", "Wilmington", "Marcus Hook", "Jefferson Station", "Suburban Station", "30th"],
    "WTR": ["West Trenton", "Jefferson Station", "Suburban Station", "30th"],
}

def all_off():
    for led in LEDS.values():
        led.off()

def display_route(route, step_delay=0.4, hold=1.0):
    stops = ROUTE_STOP_ORDER[route]
    name = ROUTE_NAMES.get(route, route)
    print(f"Route: {name} ({route}) — {len(stops)} stops")

    # Light up stops one at a time from terminus inward
    for stop in stops:
        LEDS[stop].on()
        time.sleep(step_delay)

    # Hold all on
    time.sleep(hold)

    # Turn them off back out toward the terminus
    for stop in reversed(stops):
        LEDS[stop].off()
        time.sleep(step_delay / 2)

    time.sleep(0.3)

def main():
    try:
        print("Starting route display (terminus inward)...")
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
