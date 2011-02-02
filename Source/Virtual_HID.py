import time

from ctypes import *
from ctypes.wintypes import *

#Global c_ulong pointer object used with
#dwExtraInfo in certain structs. Might be a
#better idea to convert this into a class,
#but it works well as it is.
PUL = POINTER(c_ulong)

class KeyBdInput(Structure):
    """Creates a keyboard input structure. wVk is the virtual
       keycode which correspond to physical keys. wScan, dwFlags
       and time may be left at 0. dwExtraInfo is a pointer to a
       ulong data type holding extra information on our action.
       Info on virtual key codes can be found at
       ttp://msdn.microsoft.com/en-us/library/ms927178.aspx
       """
       
    _fields_ = [("wVk", c_ushort),
             ("wScan", c_ushort),
             ("dwFlags", c_ulong),
             ("time", c_ulong),
             ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
    """HardwareInput is unused in this module, but is
       provided for completeness (for the Input Interface)."""
       
    _fields_ = [("uMsg", c_ulong),
             ("wParamL", c_short),
             ("wParamH", c_ushort)]

class MouseInput(Structure):
    """Creates a mouse input structure. dx and dy are mouse
       coordinates. They can be left at 0, as can mouseData
       and time. dwExtraInfo is a pointer to a ulong data type
       holding extra information on our action.
       dwFlags is the click value of the virtual mouse. Info
       can be found at 
       http://msdn.microsoft.com/en-us/library/ms927178.aspx
       """

    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("mouseData", c_ulong),
             ("dwFlags", c_ulong),
             ("time",c_ulong),
             ("dwExtraInfo", PUL)]

class Input_I(Union):
    """Input interface, takes one the following
       structs: KeyBdInput, MouseInput, HardwareInput."""
       
    _fields_ = [("ki", KeyBdInput),
              ("mi", MouseInput),
              ("hi", HardwareInput)]

class Input(Structure):
    """Input is the final struct we use before passing
       the information off to the OS. The type field takes
       a 0 or 1 for mouse or keyboard respectively. """
       
    _fields_ = [("type", c_ulong),
             ("ii", Input_I)]
    
class KeyBdState(Structure):
    """This is a C type 256-byte array used for storing
       the current state of our virtual keyboard. With the
       exception of toggle keys (CAPS LOCK, SCROLL LOCK, etc),
       many keys will be in the '0' state. """
       
    _fields_ = [("array", c_byte * 256)]

class VKeyboard():
    """Our Virtual Keyboard! Takes type speed as its
       only (optional) argument. Default is 0.3 seconds."""
       
    def __init__(self, typeSpeed = 0.3):
        """Init of our VKeyboard sets up an ulong for
           extra information provided by the operating system,
           an Input Interface object and the virtual key code
           table."""

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
        """[Private] Takes a virtual key code and sends it to
           the operating system. """
           
        self.click.ki = KeyBdInput(key, 0, 0, 0, pointer(self.extra))
        x = Input(1, self.click)
        windll.user32.SendInput(1, pointer(x), sizeof(x))
        time.sleep(self.typeSpeed)
        
    def _getKeyboardState(self):
        """[Private] Returns the state of our virtual keyboard in
           a 256-byte C array."""
        
        k = KeyBdState()
        windll.user32.GetKeyboardState(pointer(k))
        return k

    def translateKey(self, key):
        """Translate a virtual key code into an actual 'keyboard
           key'."""
           
        if self.vKeyTable.has_key(key):
            return self.vKeyTable.get(key)
        else:
            raise ValueError

    def pressButton(self, button):
        """Takes a physical key representation (e.g. 'ESCAPE', 'UP',
           'DOWN', 'v', etc.) and translates it into a virtual key
           code for use by the OS. """
           
        try:
            self._type(self.translateKey(button))
        except ValueError:
            print("Cannot translate key: Value Error!")

def moveCircle():
    """Move the mouse in the largest circle possible for the
       given screen resolution and continues in decreasing spiral
       sizes of 1 pixel. Prints how many circles have been made,
       and how many iterations of the spriral/circle have been made.
       Just an example of mouse movement."""
    
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

    import math

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
        """Init of our VMouse sets up an ulong for
           extra information provided by the operating system,
           an Input Interface object and a virtual click table."""
        
        self.click = Input_I()
        self.extra = c_ulong(0)
        self.clickSpeed = clickSpeed

        #In general, we will want to click a button and
        #release it in order to simulate a single click
        self.clickTable = { 'left': [0x02, 0x04],
                            'right': [0x08, 0x10],
                            'middle': [0x20, 0x40]
                          }
        
    def getCoord(self):
        """Gets the current mouse coordinates from the OS.
           Returns a POINT object."""
           
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return pt

    def setCoord(self, xCoord, yCoord):
        """Pass coordinates to the OS to set the mouse at
           the desired coordinates."""
           
        windll.user32.SetCursorPos(xCoord, yCoord)

    def _click(self, clickValues):
        """[Private] Send a virtual key code representing a click
           to the operating system, followed by {clickSpeed} seconds
           sleep, followed by a click release."""

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
        """Translate our click type to virtual key codes representing
           a click and release tuple."""
           
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
    
if __name__ == '__main__':
    m = VMouse()
    k = VKeyboard()