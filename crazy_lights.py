import time
import random

from gpiozero import LED

from mappings import STOPS_TO_PINS

LEDS = {stop: LED(pin) for stop, pin in STOPS_TO_PINS.items()}

# Stations shared by nearly every route — the downtown spine
DOWNTOWN_CORRIDOR = ["30th", "Suburban Station", "Jefferson Station"]

# Secondary interchange hubs
SECONDARY_HUBS = ["Wayne Junction", "Glenside", "North Broad", "North Philadelphia"]

# Terminal stops — the outer ends of each route
TERMINI = [
    "Thorndale", "Cynwyd", "Norristown", "Chestnut Hill West", "Chestnut Hill East",
    "Doylestown", "Lansdale", "Warminster", "West Trenton", "Fox Chase",
    "Airport", "Wawa", "Newark DE", "Wilmington", "Marcus Hook", "Trenton",
]

# Each route's stops ordered from terminus inward to 30th Street
ROUTES_INWARD = [
    ["Thorndale", "Malvern", "Paoli", "Bryn Mawr", "30th"],
    ["Chestnut Hill East", "Wayne Junction", "Jefferson Station", "Suburban Station", "30th"],
    ["Chestnut Hill West", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    ["Cynwyd", "Suburban Station", "30th"],
    ["Fox Chase", "Wayne Junction", "Jefferson Station", "Suburban Station", "30th"],
    ["Doylestown", "Lansdale", "West Trenton", "Glenside", "Wayne Junction", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    ["Doylestown", "Lansdale", "Glenside", "Wayne Junction", "North Philadelphia", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    ["Wawa", "Jefferson Station", "Suburban Station", "30th"],
    ["Norristown", "North Broad", "Jefferson Station", "Suburban Station", "30th"],
    ["Trenton", "North Philadelphia", "Jefferson Station", "Suburban Station", "30th"],
    ["Warminster", "Glenside", "Wayne Junction", "Jefferson Station", "Suburban Station", "30th"],
    ["Newark DE", "Wilmington", "Marcus Hook", "Jefferson Station", "Suburban Station", "30th"],
    ["West Trenton", "Jefferson Station", "Suburban Station", "30th"],
    ["Airport", "Jefferson Station", "Suburban Station", "30th"],
]

def all_on():
    for led in LEDS.values():
        led.on()

def all_off():
    for led in LEDS.values():
        led.off()

def light_group(stops, delay=0.0):
    for stop in stops:
        if stop in LEDS:
            LEDS[stop].on()
    if delay:
        time.sleep(delay)

def off_group(stops, delay=0.0):
    for stop in stops:
        if stop in LEDS:
            LEDS[stop].off()
    if delay:
        time.sleep(delay)

def hub_pulse(flashes=6, delay=0.12):
    """Strobe only the downtown corridor — the beating heart of the network."""
    for _ in range(flashes):
        light_group(DOWNTOWN_CORRIDOR, delay)
        off_group(DOWNTOWN_CORRIDOR, delay)

def diverge(step_delay=0.5, hold=0.8):
    """Energy radiates outward from downtown through hubs to termini."""
    all_off()
    light_group(DOWNTOWN_CORRIDOR, step_delay)
    light_group(SECONDARY_HUBS, step_delay)
    light_group(TERMINI, hold)
    off_group(TERMINI, step_delay / 2)
    off_group(SECONDARY_HUBS, step_delay / 2)
    off_group(DOWNTOWN_CORRIDOR)

def converge(step_delay=0.5, hold=0.8):
    """All termini light up and energy flows inward to downtown."""
    all_off()
    light_group(TERMINI, step_delay)
    light_group(SECONDARY_HUBS, step_delay)
    light_group(DOWNTOWN_CORRIDOR, hold)
    off_group(DOWNTOWN_CORRIDOR, step_delay / 2)
    off_group(SECONDARY_HUBS, step_delay / 2)
    off_group(TERMINI)

def train_run(route_stops, delay=0.15):
    """Simulate a single train moving along a route — one LED at a time."""
    prev = None
    for stop in route_stops:
        if prev and prev in LEDS:
            LEDS[prev].off()
        if stop in LEDS:
            LEDS[stop].on()
        prev = stop
        time.sleep(delay)
    time.sleep(delay)
    if prev and prev in LEDS:
        LEDS[prev].off()

def all_trains(delay=0.12):
    """Run every route as a train simultaneously (step-locked, not threaded)."""
    # Pad routes to the same length
    max_len = max(len(r) for r in ROUTES_INWARD)
    padded = [r + [None] * (max_len - len(r)) for r in ROUTES_INWARD]

    prev_stops = [None] * len(ROUTES_INWARD)
    for step in range(max_len + 1):
        for i, route in enumerate(padded):
            prev = prev_stops[i]
            curr = route[step] if step < len(route) else None
            if prev and prev in LEDS:
                LEDS[prev].off()
            if curr and curr in LEDS:
                LEDS[curr].on()
            prev_stops[i] = curr
        time.sleep(delay)

    # Ensure all off after
    all_off()

def strobe_hubs(flashes=16, delay=0.05):
    """Strobe hubs and termini alternately."""
    for _ in range(flashes):
        light_group(DOWNTOWN_CORRIDOR + SECONDARY_HUBS)
        off_group(TERMINI)
        time.sleep(delay)
        off_group(DOWNTOWN_CORRIDOR + SECONDARY_HUBS)
        light_group(TERMINI)
        time.sleep(delay)
    all_off()

def random_train(duration=5, delay=0.15):
    """Random trains run on random routes for a given duration."""
    end = time.time() + duration
    while time.time() < end:
        route = random.choice(ROUTES_INWARD)
        if random.random() > 0.5:
            route = list(reversed(route))
        train_run(route, delay)

def main():
    try:
        print("Going crazy (SEPTA edition)...")
        while True:
            print("Hub pulse!")
            hub_pulse(flashes=10, delay=0.1)
            time.sleep(0.3)

            print("Diverge from downtown!")
            for _ in range(3):
                diverge(step_delay=0.4, hold=0.6)

            print("Converge to downtown!")
            for _ in range(3):
                converge(step_delay=0.4, hold=0.6)

            print("All trains inward!")
            all_trains(delay=0.15)
            time.sleep(0.4)

            print("All trains outward!")
            outward = [list(reversed(r)) for r in ROUTES_INWARD]
            max_len = max(len(r) for r in outward)
            padded = [r + [None] * (max_len - len(r)) for r in outward]
            prev_stops = [None] * len(outward)
            for step in range(max_len + 1):
                for i, route in enumerate(padded):
                    prev = prev_stops[i]
                    curr = route[step] if step < len(route) else None
                    if prev and prev in LEDS:
                        LEDS[prev].off()
                    if curr and curr in LEDS:
                        LEDS[curr].on()
                    prev_stops[i] = curr
                time.sleep(0.15)
            all_off()
            time.sleep(0.4)

            print("Strobe hubs vs termini!")
            strobe_hubs(flashes=20, delay=0.06)
            time.sleep(0.3)

            print("Random trains!")
            random_train(duration=5, delay=0.12)

            print("Ping pong — diverge/converge!")
            for _ in range(4):
                diverge(step_delay=0.25, hold=0.3)
                converge(step_delay=0.25, hold=0.3)

    except KeyboardInterrupt:
        print("\nCalming down...")
        all_off()

if __name__ == "__main__":
    main()

