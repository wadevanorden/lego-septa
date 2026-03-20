from gpiozero import LED

pins = [LED(pin) for pin in range(26)]

for pin in pins:
    pin.on()

input("All pins 0-25 are ON. Press Enter to turn them off...")

for pin in pins:
    pin.off()
