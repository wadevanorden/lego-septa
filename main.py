import time

import requests
from gpiozero import LED

from mappings import AIRPORT_STOPS, NORTH_PHILLY_STOPS, STOPS, STOPS_TO_PINS

# Store LED objects to reuse them
LEDS = {stop: LED(pin) for stop, pin in STOPS_TO_PINS.items()}

def main():
    try:
        while True:
            regionalRails = getRegionalRails()
            stopStatus = findStopStatuses(regionalRails)
            offLights()
            setLights(stopStatus)
            time.sleep(15)
            offLights()
    except KeyboardInterrupt:
        print("\nExiting...")
        offLights()

def offLights():
    for stop in STOPS_TO_PINS.keys():
        LEDS[stop].off()

def getRegionalRails():
    response = requests.get('https://api.septa.org/api/TrainView/')
    if response.status_code == 200:
        return response.json()
    
def filterRegionalRails(regionalRails):
    seenLines = []
    filteredRegionalRails = []

    for train in regionalRails:
        if train['service'] == 'LOCAL':
            filteredRegionalRails.append(train)
            seenLines.append(train['line'])

    return filteredRegionalRails

def findStopStatuses(regionalRails):
    stopStatus = {}

    for stop in STOPS:
        stopStatus[stop] = 0

    for train in regionalRails:
        if stopStatus.get(train['currentstop']) == 2 or stopStatus.get(train['nextstop']) == 2:
            continue
        if train['currentstop'] in STOPS:
            stopStatus[train['currentstop']] = 2
        elif train['nextstop'] in STOPS:
            stopStatus[train['nextstop']] = 1
    
    return stopStatus

def setLights(stopStatus):
    airportValue = 0
    northPhillyValue = 0

    for stop in AIRPORT_STOPS:
        airportValue = max(stopStatus.get(stop), airportValue)
    for stop in NORTH_PHILLY_STOPS:
        northPhillyValue = max(stopStatus.get(stop), northPhillyValue)

    for stop in STOPS_TO_PINS.keys():
        if stop in AIRPORT_STOPS or stop in NORTH_PHILLY_STOPS:
            continue
        else:
            print(f"Setting {stop} to {stopStatus.get(stop, 0)}")
            if stopStatus.get(stop, 0) == 2:
                LEDS[stop].on()
            elif stopStatus.get(stop, 0) == 1:
                LEDS[stop].blink(on_time=0.5, off_time=0.5)
            else:
                LEDS[stop].off()

    if airportValue == 2:
        LEDS["Airport"].on()
    elif airportValue == 1:
        LEDS["Airport"].blink(on_time=0.5, off_time=0.5)
    else:
        LEDS["Airport"].off()
    
    if northPhillyValue == 2:
        LEDS["North Philadelphia"].on()
    elif northPhillyValue == 1:
        LEDS["North Philadelphia"].blink(on_time=0.5, off_time=0.5)
    else:
        LEDS["North Philadelphia"].off()

if __name__ == "__main__":    main()