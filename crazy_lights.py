import time
import random

from gpiozero import LED

from mappings import STOPS_TO_PINS

LEDS = {stop: LED(pin) for stop, pin in STOPS_TO_PINS.items()}
STOPS = list(STOPS_TO_PINS.keys())

def all_on():
    for led in LEDS.values():
        led.on()

def all_off():
    for led in LEDS.values():
        led.off()

def wave(delay=0.05):
    for stop in STOPS:
        LEDS[stop].on()
        time.sleep(delay)
    for stop in STOPS:
        LEDS[stop].off()
        time.sleep(delay)

def reverse_wave(delay=0.05):
    for stop in reversed(STOPS):
        LEDS[stop].on()
        time.sleep(delay)
    for stop in reversed(STOPS):
        LEDS[stop].off()
        time.sleep(delay)

def strobe(flashes=20, delay=0.05):
    for _ in range(flashes):
        all_on()
        time.sleep(delay)
        all_off()
        time.sleep(delay)

def random_chaos(duration=5, delay=0.05):
    end = time.time() + duration
    while time.time() < end:
        stop = random.choice(STOPS)
        if random.random() > 0.5:
            LEDS[stop].on()
        else:
            LEDS[stop].off()
        time.sleep(delay)

def ping_pong(cycles=3, delay=0.05):
    for _ in range(cycles):
        wave(delay)
        reverse_wave(delay)

def cascade_blink(on_time=0.2, off_time=0.1):
    for stop in STOPS:
        LEDS[stop].blink(on_time=on_time, off_time=off_time)
        time.sleep(0.05)

def stop_blink():
    for led in LEDS.values():
        led.off()

def main():
    try:
        print("Going crazy...")
        while True:
            print("Strobe!")
            strobe(flashes=30, delay=0.04)

            print("Wave!")
            for _ in range(4):
                wave(delay=0.04)

            print("Reverse wave!")
            for _ in range(4):
                reverse_wave(delay=0.04)

            print("Ping pong!")
            ping_pong(cycles=3, delay=0.05)

            print("Random chaos!")
            random_chaos(duration=4, delay=0.03)

            print("Cascade blink!")
            cascade_blink()
            time.sleep(3)
            stop_blink()

            print("Strobe again!")
            strobe(flashes=20, delay=0.06)

    except KeyboardInterrupt:
        print("\nCalming down...")
        stop_blink()
        all_off()

if __name__ == "__main__":
    main()
