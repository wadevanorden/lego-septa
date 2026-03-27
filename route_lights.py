import time

from gpiozero import LED

from mappings import STOPS_TO_PINS, STOPS_TO_ROUTES, ROUTES

# Build LED objects for each mapped stop
LEDS = {stop: LED(pin) for stop, pin in STOPS_TO_PINS.items()}

# Invert STOPS_TO_ROUTES to get ROUTES_TO_STOPS, preserving STOPS_TO_PINS order
ROUTES_TO_STOPS = {route: [] for route in ROUTES}
for stop in STOPS_TO_PINS:
    for route in STOPS_TO_ROUTES.get(stop, []):
        if route in ROUTES_TO_STOPS:
            ROUTES_TO_STOPS[route].append(stop)

ROUTE_NAMES = {
    "AIR": "Airport",
    "CHE": "Chestnut Hill East",
    "CHW": "Chestnut Hill West",
    "CYN": "Cynwyd",
    "FOX": "Fox Chase",
    "GLN": "Lansdale/Doylestown",
    "LAN": "Lansdale/Doylestown",
    "MED": "Media/Wawa",
    "NOR": "Norristown",
    "PAO": "Paoli/Thorndale",
    "TRE": "Trenton",
    "WAR": "Warminster",
    "WIL": "Wilmington/Newark",
    "WTR": "West Trenton",
}

def all_off():
    for led in LEDS.values():
        led.off()

def display_route(route, step_delay=0.4, hold=1.0):
    stops = ROUTES_TO_STOPS[route]
    name = ROUTE_NAMES.get(route, route)
    print(f"Route: {name} ({route}) — {len(stops)} stops")

    # Light up stops one at a time along the route
    for stop in stops:
        LEDS[stop].on()
        time.sleep(step_delay)

    # Hold all on
    time.sleep(hold)

    # Turn them off one at a time
    for stop in stops:
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
