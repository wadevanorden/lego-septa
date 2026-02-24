import requests
from gpiozero import LED

from mappings import AIRPORT_STOPS, NORTH_PHILLY_STOPS, STOPS, STOPS_TO_PINS

def main():
    regionalRails = getRegionalRails()
    stopStatus = findStopStatuses(regionalRails)
    setLights(stopStatus)

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
            print(f"Train is currently at {train['currentstop']}")
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

    for stop, pin in STOPS_TO_PINS.items():
        if stop in AIRPORT_STOPS or stop in NORTH_PHILLY_STOPS:
            continue
        else:
            if stopStatus.get(stop, 0) == 2:
                LED(pin).on()
            elif stopStatus.get(stop, 0) == 1:
                LED(pin).blink(on_time=0.5, off_time=0.5)
            else:
                LED(pin).off()

    if airportValue == 2:
        LED(STOPS_TO_PINS["Airport"]).on()
    elif airportValue == 1:
        LED(STOPS_TO_PINS["Airport"]).blink(on_time=0.5, off_time=0.5)
    else:
        LED(STOPS_TO_PINS["Airport"]).off()
    
    if northPhillyValue == 2:
        LED(STOPS_TO_PINS["North Philadelphia"]).on()
    elif northPhillyValue == 1:
        LED(STOPS_TO_PINS["North Philadelphia"]).blink(on_time=0.5, off_time=0.5)
    else:
        LED(STOPS_TO_PINS["North Philadelphia"]).off()

if __name__ == "__main__":    main()