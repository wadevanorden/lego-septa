import time
import random

from gpiozero import LED

from mappings import STOPS_TO_PINS

LEDS = {stop: LED(pin) for stop, pin in STOPS_TO_PINS.items()}

# Stations shared by nearly every route — the downtown spine
DOWNTOWN_CORRIDOR = ["30th", "Suburban Station", "Jefferson Station"]

HUBS = ["30th", "Suburban Station", "Jefferson Station", "Thorndale", "Cynwyd", "Norristown", "Chestnut Hill West", "Chestnut Hill East", "Doylestown", "Warminster", "West Trenton", "Fox Chase", "Airport", "Wawa", "Newark DE", "Trenton"]

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

def highlight_hubs(hold=3):
    """Light up all hub stations."""
    all_off()
    light_group(HUBS, hold)
    off_group(HUBS)

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

def transfer_at_30th(hops=6, delay=0.15):
    """Train arrives at 30th, then repeatedly picks a random onward route and returns."""
    all_off()
    # Arrive at 30th on a random inbound route
    arrival = list(reversed(random.choice(ROUTES_INWARD)))  # outward → inward
    train_run(arrival, delay)

    used = None
    for _ in range(hops):
        # Pick a random route that doesn't immediately repeat
        choices = [r for r in ROUTES_INWARD if r is not used]
        route_out = random.choice(choices)
        used = route_out
        # Run outward from 30th (inward list reversed = outward)
        train_run(list(reversed(route_out)), delay)
        # Run back inward to 30th
        train_run(route_out, delay)

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
            print("Highlight hubs!")
            highlight_hubs(hold=10)
            time.sleep(0.3)

            print("All trains inward!")
            all_trains(delay=0.15)
            time.sleep(0.4)

            print("Transfer at 30th!")
            transfer_at_30th(hops=6, delay=0.15)
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

            print("Random trains!")
            random_train(duration=5, delay=0.12)

    except KeyboardInterrupt:
        print("\nCalming down...")
        all_off()

if __name__ == "__main__":
    main()

