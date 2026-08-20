from machine import Pin
import time
import random
class whackamole:
    def __init__(self):
        self.ledlist = [
            Pin(28, Pin.OUT),
            Pin(27, Pin.OUT),
            Pin(26, Pin.OUT),
            Pin(22, Pin.OUT)
            ]
    
        self.buttonlist = [
            Pin(3, Pin.IN, Pin.PULL_DOWN),
            Pin(2, Pin.IN, Pin.PULL_DOWN),
            Pin(1, Pin.IN, Pin.PULL_DOWN),
            Pin(0, Pin.IN, Pin.PULL_DOWN),
            ]

        # store the button value at start
        self.oldbuttonstate = [self.buttonlist[z].value() for z in range(4)]

        #light a random led to start
        self.lightRandomLED()

    def lightRandomLED(self):
        for z in range(4):
            self.ledlist[z].value(0)
        newled = random.randint(0,3)
        self.ledlist[newled].value(1)

    def catchButtons(self):
    
        # check if any of the buttons have flipped their state        
        newbuttonstate = [self.buttonlist[z].value() for z in range(4)]

        for z in range(4):
            if self.oldbuttonstate[z] == 0 and newbuttonstate[z] == 1:
                # a button press was detected, now check if the led is on
                if self.ledlist[z].value() == 1:
                    #turn it off and pick a new one
                    self.ledlist[z].value(0)
                    self.lightRandomLED()
                print(f'Button {z} was pressed')

        self.oldbuttonstate = newbuttonstate
        
        time.sleep(0.01)

print("Program is running")
driver = whackamole()
while True:
    driver.catchButtons()
