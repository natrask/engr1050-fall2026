import math
from machine import ADC, Pin
import time


# A class to catch when buttons are pressed
class ButtonClass:
    """
    A class to detect button press events on a Raspberry Pi Pico.
    
    This class handles button debouncing and edge detection, returning True
    only when a button press event occurs (transition from not pressed to pressed).
    """
    
    def __init__(self, pin_number):
        """
        Initialize the button class.
        
        Args:
            pin_number (int): GPIO pin number where the button is connected
            
        Note:
            Button should be wired with one side to the specified pin and 
            the other side to 3.3V. The internal pull-down resistor is enabled.
        """
        self.button = Pin(pin_number, Pin.IN, Pin.PULL_DOWN)
        
        # Store the button value at start to detect state changes
        self.oldbuttonstate = self.button.value() 

    def catchPress(self):
        """
        Check if a button press event has occurred.
        
        This method detects the rising edge of a button press (transition from 
        low to high) and returns True only once per press event.
        
        Returns:
            bool: True if a button press was detected, False otherwise
            
        Note:
            This method includes a small delay (0.01s) for basic debouncing.
            It should be called repeatedly in a loop to monitor button state.
        """
        # Check if any of the buttons have flipped their state        
        newbuttonstate = self.button.value()

        if self.oldbuttonstate == 0 and newbuttonstate == 1:
            # A button press was detected (rising edge)
            self.oldbuttonstate = newbuttonstate
            return True

        # Update the old state for next iteration
        self.oldbuttonstate = newbuttonstate
        
        # Small delay for debouncing
        time.sleep(0.01)
        return False


class LEDClass:
    def __init__(self, pin_number, initial_state=False):
        """
        Initialize LED class
        pin_number: GPIO pin number for the LED
        initial_state: True for on, False for off (default: False)
        """
        self.led = Pin(pin_number, Pin.OUT)
        self.state = initial_state
        
        # Set initial state
        if self.state:
            self.led.on()
        else:
            self.led.off()
    
    def toggle(self):
        """Toggle the LED state (on->off or off->on)"""
        if self.state:
            self.led.off()
            self.state = False
        else:
            self.led.on()
            self.state = True
            
print("Program is running")

# Initialize some buttons here, for example
quitButton = ButtonClass(pin_number=0)
increaseButton = ButtonClass(pin_number=1)
decreaseButton = ButtonClass(pin_number=2)
toggleController = ButtonClass(pin_number=3)

# Initialize the LEDs here, for example
ontargetLED = LEDClass(pin_number=16)
poweronLED = LEDClass(pin_number=17)

# Initialize potentiometer
potentiometer = ADC(Pin(26))

# Set the initial state for the controller
controllerAngle = 45   # target 45 degrees to start
controllerOn = False            # Start with controller turned off

theta0 = 34000
theta90 = 9200
while True:
    # Read potentiometer and convert reading to angle
    pot_value = potentiometer.read_u16() # Read the ADC value (0-65535)
    theta_value = 90.0*(pot_value-theta0)/(theta90-theta0) # Modify this line to convert from a raw voltage to an angle

    # Capture button pressing events 
    quitPressed = quitButton.catchPress() 
    increasePressed = increaseButton.catchPress()
    decreasePressed = decreaseButton.catchPress()
    togglePressed = toggleController.catchPress()

    # Capture potentiometer input
    currentTheta = theta_value
    onTarget = abs(currentTheta - controllerAngle) < 5 # Check whether we're within 5 degrees
    if onTarget != ontargetLED.state:
        ontargetLED.toggle()
        
    # Add/subtract 5 degrees to target if button pressed
    if increasePressed:
        controllerAngle += 5
    if decreasePressed:
        controllerAngle -= 5
        
    # Flip the Controller running variable if button is pressed (won't use this today)
    if togglePressed:
        controllerOn = not controllerOn
        if controllerOn != poweronLED.state:
            poweronLED.toggle()

    # Power down if the quit button was pressed
    if quitPressed == True:
        print('Turning off...')
        # Turn off the LED
        break
    
    # After executing all of the logic for the step, print out current state
    print(f'Controller running = {controllerOn}. Theta = {currentTheta}, Target = {controllerAngle}')        
    time.sleep(0.1)  # Small delay
