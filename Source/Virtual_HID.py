import time

from ctypes import *
from ctypes.wintypes import *

#(ulong) Pointer to extra info given by SendInput
#Read with:
#  ctypes.windll.user32.GetMessageExtraInfo()
#Used by:
#  KeyBdInput
#  MouseInput

#Make this into a class.
#Pointers can be stored in lists and called with __call__()

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
    
class KeyBdState(Structure):
    _fields_ = [("array", c_byte * 256)]

class VKeyboard():
    
    def __init__(self, typeSpeed = 0.3):
        self.extra = c_ulong(0)
        self.click = Input_I()
        self.typeSpeed = typeSpeed

        self.vKeyTable = { 'BACKSPACE': 0x08,
                           'TAB': 0x09,
                           'ENTER': 0x0D,
                           'SHIFT': 0x10,
                           'CTRL': 0x11,
                           'ALT': 0x12,
                           'PAUSE': 0x13,
                           'CAPSLOCK': 0x14,
                           'ESCAPE': 0x1B,
                           ' ': 0x20,
                           'SPACEBAR': 0x20,
                           'PAGEUP': 0x21,
                           'PAGEDOWN': 0x22,
                           'END': 0x23,
                           'HOME': 0x24,
                           'LEFT': 0x25,
                           'UP': 0x26,
                           'RIGHT': 0x27,
                           'DOWN': 0x28,
                           'PRINTSCR': 0x2C,
                           'INSERT': 0x2D,
                           'DELETE': 0x2E,
                           'HELP': 0x2F,
                           0: 0x30,
                           1: 0x31,
                           2: 0x32,
                           3: 0x33,
                           4: 0x34,
                           5: 0x35,
                           6: 0x36,
                           7: 0x37,
                           8: 0x38,
                           9: 0x39,
                           'A': 0x41,
                           'B': 0x42,
                           'C': 0x43,
                           'D': 0x44,
                           'E': 0x45,
                           'F': 0x46,
                           'G': 0x47,
                           'H': 0x48,
                           'I': 0x49,
                           'J': 0x4a,
                           'K': 0x4b,
                           'L': 0x4c,
                           'M': 0x4d,
                           'N': 0x4e,
                           'O': 0x4f,
                           'P': 0x50,
                           'Q': 0x51,
                           'R': 0x52,
                           'S': 0x53,
                           'T': 0x54,
                           'U': 0x55,
                           'V': 0x56,
                           'W': 0x57,
                           'X': 0x58,
                           'Y': 0x59,
                           'Z': 0x5a,
                           'LWINKEY': 0x5B,
                           'RWINKEY': 0x5C,
                           'APPKEY': 0x5D,
                           'SLEEP': 0x5F,
                           'NUM0': 0x60,
                           'NUM1': 0x61,
                           'NUM2': 0x62,
                           'NUM3': 0x63,
                           'NUM4': 0x64,
                           'NUM5': 0x65,
                           'NUM6': 0x66,
                           'NUM7': 0x67,
                           'NUM8': 0x68,
                           'NUM9': 0x69,
                           'MULTIPLY': 0x6A,
                           'ADD': 0x6B,
                           'SEP': 0x6C,
                           'SUB': 0x6D,
                           'DECIMAL': 0x6E,
                           'DIVIDE': 0x6E,
                           'F1': 0x70,
                           'F2': 0x71,
                           'F3': 0x72,
                           'F4': 0x73,
                           'F5': 0x74,
                           'F6': 0x75,
                           'F7': 0x76,
                           'F8': 0x77,
                           'F9': 0x78,
                           'F10': 0x79,
                           'F11': 0x7a,
                           'F12': 0x7b,
                           'F13': 0x7c,
                           'F14': 0x7d,
                           'F15': 0x7e,
                           'F16': 0x7f,
                           'F17': 0x80,
                           'F18': 0x81,
                           'F19': 0x82,
                           'F20': 0x83,
                           'F21': 0x84,
                           'F22': 0x85,
                           'F23': 0x86,
                           'F24': 0x87,
                           'NUMLOCK': 0x90,
                           'SCROLL': 0x91,
                           'LSHIFT': 0xA0,
                           'RSHIFT': 0xA1,
                           'LCTRL': 0xA2,
                           'RCTRL': 0xA3,
                           'LMENU': 0xA4,
                           'RMENU': 0xA5,

                           #Browser Buttons
                           'B_Back': 0xA6,
                           'B_Forward': 0xA7,
                           'B_Refresh': 0xA8,
                           'B_Stop': 0xA9,
                           'B_Search': 0xAA,
                           'B_Favorites': 0xAB,

                           'VOL_MUTE': 0xAD,
                           'VOL_DOWN': 0xAE,
                           'VOL_UP': 0xAF,
                           'NEXT_TRACK': 0xB0,
                           'PREV_TRACK': 0xB1,
                           'STOP_TRACK': 0xB2,
                           'PLAY_PAUSE': 0xB3,
                           'MAIL': 0xB4,
                           
                        }
                           
                           
    
    def _type(self, key):
        self.click.ki = KeyBdInput(key, 0, 0, 0, pointer(self.extra))
        x = Input(1, self.click)
        windll.user32.SendInput(1, pointer(x), sizeof(x))
        time.sleep(self.typeSpeed)
        
    def _getKeyboardState(self):
        
        #Need to translate this into keys
        
        k = KeyBdState()
        windll.user32.GetKeyboardState(pointer(k))
        for x in k.array:
            print x

    def translateKey(self, key):
        if self.vKeyTable.has_key(key):
            return self.vKeyTable.get(key)
        else:
            raise ValueError

    def pressButton(self, button):
        try:
            self._type(self.translateKey(button))
        except ValueError:
            print("Cannot translate key: Value Error!")

def moveCircle():
    m = VMouse()
    screenRes = windll.user32.GetSystemMetrics(0), \
                windll.user32.GetSystemMetrics(1)
    center = [(screenRes[0]//2), (screenRes[1]//2)]

    if screenRes[0] < screenRes[1]:
        radius = screenRes[0]//2
    else:
        radius = screenRes[1]//2

    maxRadius = radius   
    iters, spirals = 0, 0

    import math, time

    while True:
        for degree in range(360):
            x = center[0] + int(radius*math.cos((degree*(math.pi/180))))
            y = center[1] + int(radius*math.sin((degree*(math.pi/180))))
            m.setCoord(x, y)
            time.sleep(0.001)
        radius = radius - 1
        if radius is 0:
            radius = maxRadius
            spirals += 1
            print spirals, "spirals made!"
        iters += 1
        if not iters % 100:
            print iters, " iterations made!"

class VMouse():

    """
    Create a virtual mouse.
    Click speed is the amount of time between pressing down a
    mouse button and releasing it. Default is 0.5 seconds.
    """

    def __init__(self, clickSpeed = 0.5):
        self.click = Input_I()
        self.extra = c_ulong(0)
        self.clickSpeed = clickSpeed

        #Click table is shown as:
        #buttonType: [clickValue, releaseValue]
        self.clickTable = { 'left': [0x02, 0x04],
                            'right': [0x08, 0x10],
                            'middle': [0x20, 0x40]
                          }
        
    def getCoord(self):
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt

    def setCoord(self, xCoord, yCoord):
        windll.user32.SetCursorPos(xCoord, yCoord)

    def _click(self, clickValues):
        
        # Possible Click Values
        # =====================
        # Left Click:     0x02
        # Left Release:   0x04
        # Right Click:    0x08
        # Right Release:  0x10
        # Middle Click:   0x20
        # Middle Release: 0x40

        i = 0
        for values in clickValues:
            self.click.mi = MouseInput(0, 0, 0, clickValues[i], 0, pointer(self.extra))
            x = Input(0, self.click)
            windll.user32.SendInput(1, pointer(x), sizeof(x))
            time.sleep(self.clickSpeed)
            i += 1

    def leftClick(self):
        clickValues = self.translateClick('left')
        self._click(clickValues)

    def rightClick(self):
        clickValues = self.translateClick('right')
        self._click(clickValues)

    def middleClick(self):
        clickValues = self.translateClick('middle')
        self._click(clickValues)

    def translateClick(self, buttonToClick):
        if self.clickTable.has_key(buttonToClick):
            return self.clickTable.get(buttonToClick)
        else:
            raise ValueError

    def _mouseWheel(self):
        pass

    def mouseWheelUp(self, amt):
        pass

    def mouseWheelDown(self, amt):
        pass

def demo():

    """Quick demo to open notepad and type some input."""

    import time

    #Initialize our Virtual HIDs
    k = VKeyboard(typeSpeed=0.01)
    m = VMouse()

    #Start Menu button coords
    xCoord, yCoord = 16, 726
    applications = ['notepad', 'scite']

    for app in applications:
        #Click start menu
        m.setCoord(xCoord, yCoord)
        m.leftClick()

        #Type our application name and press enter
        for letter in app:
            if letter.isalpha():
                k.pressButton(letter.upper())
            else:
                k.pressButton(letter)

        time.sleep(1.0)
        k.pressButton('ENTER')

        time.sleep(3.0)

        #Say the magic words
        message = "Automating user input"
        for letter in message:
            if letter.isalpha():
                k.pressButton(letter.upper())
            else:
                k.pressButton(letter)

        time.sleep(3)

        if app is 'notepad':
            m.setCoord(995, 46)
            m.leftClick()
            m.setCoord(545, 362)
            m.leftClick()
            
        if app is 'scite':
            m.setCoord(542, 6)
            m.leftClick()
            m.setCoord(506, 434)
            m.leftClick()
    del k, m


k = VKeyboard()
k._getKeyboardState()
m = VMouse()
pt = m.setCoord(480, 411)
m.leftClick()
#k.pressButtons('ALT', 'LCTRL', 'DELETE')
#k.pressButton('LCTRL')
#k.pressButton('ALT')
#k.pressButton(4)