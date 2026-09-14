# blink.py - ENGR 1050 Lecture 5
# The "hello, world" of the Raspberry Pi Pico: turn an LED on and off forever.
#
# Run this from Thonny with the interpreter set to
# "MicroPython (Raspberry Pi Pico)". See pico_blink.html for setup.
#
# To stop it, click the red Stop button in Thonny.

from machine import Pin   # Pin represents one physical pin on the Pico
import time               # time.sleep(seconds) pauses the program

# Pick which LED to blink by changing this one line.
#   Pin(25, Pin.OUT)      the green LED soldered onto the Pico itself
#   Pin("LED", Pin.OUT)   same thing, but also works on a Pico W
#   Pin(0, Pin.OUT)       an LED you wired to GP0 (see the wiring section)
led = Pin(25, Pin.OUT)

on_time = 0.5    # seconds the LED stays lit
off_time = 0.5   # seconds the LED stays dark

while True:
    led.value(1)          # 3.3 volts on the pin: LED on
    time.sleep(on_time)
    led.value(0)          # 0 volts on the pin: LED off
    time.sleep(off_time)
