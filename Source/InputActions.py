from ctypes import *
from ctypes.wintypes import *
#Mouse Events here:
#http://msdn.microsoft.com/en-us/library/ms646260(VS.85).aspx

#First we must set up C Structs to send data (KeyBdInput, etc),
#then a Union (like a struct with only one active field at any time),
#and then an Input structure to actually send to the SendInput() function


PUL = POINTER(c_ulong)
class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
             ("wScan", c_ushort),
             ("dwFlags", c_ulong),
             ("time", c_ulong),
             ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
             ("wParamL", c_short),
             ("wParamH", c_ushort)]

class MouseInput(Structure):
    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("mouseData", c_ulong),
             ("dwFlags", c_ulong),
             ("time",c_ulong),
             ("dwExtraInfo", PUL)]

class Input_I(Union):
    _fields_ = [("ki", KeyBdInput),
              ("mi", MouseInput),
              ("hi", HardwareInput)]

class Input(Structure):
    _fields_ = [("type", c_ulong),
             ("ii", Input_I)]

    """
    Input takes the Input Interface,
    and a type, where types is:
    0: Mouse
    1: Keyboard
    2: Hardware
    """

#ctypes.windll.user32.SendInput(n, arrayInputStructs, sizeof(arrayInputStructs))
#Input takes an interface reference and a type (HW, KB or Mouse)
#Input_I interfaces with the three Input types.

"""
###################
#Sample right click
###################

#Create a c_ulong to store extra info on mouse
extra = c_ulong(0)

#Create the interface
click = Input_I()
#We want to use mi (mouse), and then send MouseInput to that
click.mi = MouseInput(0, 0, 0, 8, 0, pointer(extra))

#Create an input object, which binds to click,
#and send this to SendInput()
mInput = Input(0, click)

#Now send 1 object, and a pointer to it, and it's size
windll.user32.SendInput(1, pointer(mInput), sizeof(mInput[0])

##############################################################
#The following example shows multiple clicks
#i.e. Right click, right click release
##############################################################

FInputs = Input * 2
extra = c_ulong(0)

click = Input_I()
click.mi = MouseInput(0, 0, 0, 8, 0, pointer(extra))
release = Input_I()
release.mi = MouseInput(0, 0, 0, 16, 0, pointer(extra))

x = FInputs( (0, click), (0, release) )
windll.user32.SendInput(2, pointer(x), sizeof(x[0]))

"""

class mouseActions():

    def doClick(self, button):
        
        clickType = self.getClickValue(button)
        self.sendInput(clickType)

    def releaseClick(self):
        #Value to release left/right/middle button
        releaseCodes = [0x04, 0x10, 0x40]

        buttonClicked = self.getButtonStates()

        i = 0
        for clicked in buttonClicked:
            if clicked:
                self.sendInput(releaseCodes[i])
            i += 1

    def getButtonStates(self):
        #Left/Right/Middle button clicked
        buttonStates = [0x01, 0x02, 0x04]
        buttonClicked = []
        
        for state in buttonStates:
            buttonState = windll.user32.GetKeyState(state)

            #Get our short in binary
            binaryState = bin(buttonState)
            shortState = binaryState[len(binaryState)-16:]

            #If MSB is 1, button is pressed
            if shortState[0] == '1':
                buttonClicked.append(True)
            else:
                buttonClicked.append(False)
                
        return buttonClicked

    def printButtonStates(self):
        buttons = ['Right', 'Left', 'Middle']
        buttonStates = self.getButtonStates()

        i = 0
        for x in buttonStates:
            print(buttons[i], "mouse button clicked:", buttonStates[i])
            i += 1

    def sendInput(self, clickType):
        extra = c_ulong(0)
        click = Input_I()
        click.mi = MouseInput(0, 0, 0, clickType, 0, pointer(extra))
        x = Input(0, click)
        windll.user32.SendInput(1, pointer(x), sizeof(x))

    def getClickValue(self, buttonStr):
        buttonStr = buttonStr.lower()
        if buttonStr == 'left':
            return 2
        elif buttonStr == 'right':
            return 8
        elif buttonStr == 'middle':
            return 32
