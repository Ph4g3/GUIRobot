#=========================#
#                         #
#     Version: 0.3        #
#  Author:  Martin Moore  #
#                         #
#=========================#

import time

import ctypes
from ctypes.wintypes import (c_long, c_short, c_byte, c_ulong, c_ushort, 
                             POINT, POINTER, Structure, Union, sizeof)
                   

#Global c_ulong pointer object used with
#dwExtraInfo in certain structs. Might be a
#better idea to convert this into a class,
#but it works well as it is.
PUL = POINTER(c_ulong)

class KeyBdInput(Structure):
    """Creates a keyboard input_I structure. wVk is the virtual
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
    """Creates a mouse input_I structure. dx and dy are mouse
       coordinates. They can be left at 0, as can mouseData
       and time. dwExtraInfo is a pointer to a ulong data type
       holding extra information on our action.
       dwFlags is the click value of the virtual mouse. Info
       can be found at 
       http://msdn.microsoft.com/en-us/library/ms927178.aspx
       """

    _fields_ = [("dx", c_long),
             ("dy", c_long),
             ("dwData", c_ulong),
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

        #Get our initial state so we can revert toggle keys when
        #we are done
        #
        #UPDATE: Doesn't seem like we need this - zeroing our keybdstate
        #seems to have no effect on actual interaction with the OS. This
        #is due to no Input having been sent to the OS for processing.
        #I imagine this will cause complications later:
        # - User has CAPS_LOCK toggled when vkeyboard is initialized.
        #   i.e. THEY'RE SHOUTING
        # - vkeyboard runs __init__
        # - vKeyCode for CAPS_LOCK is set to Off by program but has no
        #   effect on actual state of keyboard.
        # - User is shown that CAPS_LOCK is Off but text input from the
        #   vkeyboard will be in opposite case
        #
        #I think this might be solved by taking the states of certain keys:
        # - CAPS_LOCK
        # - PLAY_PAUSE
        # - SCROLL_LOCK
        # - Others? Do some research
        #After we apply our initial zeroing, restore state of these keys
        #so it keystates appear correctly for the user.
        
        self.initState = self._getKeyboardState()
        
        #Zero all the keys of the keyboard
        zeroState = KeyBdState()
        for button in zeroState.array:
            button = 0
        self._setKeyboardState(zeroState)
            
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
                           
    def printStates(self):
        items = self.vKeyTable.iteritems()
        values = self.vKeyTable.itervalues()
        kState = self._getKeyboardState()
        states = []
        
        i = 0
        for iterations in range(len(self.vKeyTable)):
            hexValue = values.next()
            #Hex value of vKeyCode, padded to be at least length 4
            #with leading zeros
            strValue = "0x%2.2X" % hexValue
            
            #Actual button name with leading '.'s
            item = ': '+str(items.next()[0]).rjust(12, '.')
            state = ': '+self._getKeyState(kState.array[i])
            
            #Concatenate all strings and store in list
            states.append(strValue+item+state)
            i+=1
        states.sort()
        for buttonState in states:
            print buttonState
    
    def _type(self, key):
        """[Internal] Takes a virtual key code and sends it to
           the operating system. """
           
        self.click.ki = KeyBdInput(key, 0, 0, 0, ctypes.pointer(self.extra))
        x = Input(1, self.click)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        time.sleep(self.typeSpeed)
        self._setKeyboardState(self.initState)
        
    def _getKeyboardState(self):
        """[Internal] Returns the state of our virtual keyboard in
           a 256-byte C array."""
        
        kState = KeyBdState()
        ctypes.windll.user32.GetKeyboardState(ctypes.pointer(kState))
        return kState
    
    def _setKeyboardState(self, kState):
        """[Internal] Set the state of our virtual keyboard from a
           256-byte C array."""
           
        #http://msdn.microsoft.com/en-us/library/ms646301(v=vs.85).aspx
           
        ctypes.windll.user32.SetKeyboardState(ctypes.pointer(kState))
    
    def _getKeyState(self, binKeyState):
        """[Internal] Win OS returns a short for keys state. Flags must be evaluated
           in order to determine what state the key is in."""
           
        state = ctypes.windll.user32.GetKeyState(binKeyState)
        if state is 0:
            return 'Off'
        if state is 1:
            return 'Toggled'
        return 'Pressed'
        

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
        
        self.input_I = Input_I()
        self.extra = c_ulong(0)
        self.clickSpeed = clickSpeed
        #Constant for moving mouse wheel. One 'click' forward
        #is equal to 120
        self.wheelDelta = 120

        #In general, we will want to click a button and
        #release it in order to simulate a single click
        self.clickTable = { 'left': [0x02, 0x04],
                            'right': [0x08, 0x10],
                            'middle': [0x20, 0x40],
                            'wheel': [0x800],
                            'hold_left': [0x02],
                            'release_left': [0x04],
                            'hold_right': [0x08],
                            'release_right': [0x10],
                            'hold_middle': [0x20],
                            'release_middle': [0x40]
                          }
        
    def getCoord(self):
        """Gets the current mouse coordinates from the OS.
           Returns a POINT object."""
           
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt

    def setCoord(self, xCoord, yCoord):
        """Pass coordinates to the OS to set the mouse at
           the desired coordinates."""
           
        ctypes.windll.user32.SetCursorPos(xCoord, yCoord)

    def _click(self, clickType, dwData = 0):
        """[Internal] Send a virtual key code representing a click
           to the operating system, followed by {clickSpeed} seconds
           sleep, followed by a click release."""
           
        clickValues = self._translateClick(clickType)

        for value in clickValues:
            self.input_I.mi = MouseInput(0, 0, dwData, value, 0,
                                         ctypes.pointer(self.extra))
            x = Input(0, self.input_I)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x),
                                           ctypes.sizeof(x))
            time.sleep(self.clickSpeed)
            
    def _translateClick(self, buttonToClick):
        """[Internal] Translate our click type to virtual key codes 
           representing a click and release tuple."""
           
        if self.clickTable.has_key(buttonToClick):
            return self.clickTable.get(buttonToClick)
        else:
            raise ValueError

    def leftClick(self):
        self._click('left')

    def rightClick(self):
        self._click('right')

    def middleClick(self):
        self._click('middle')
        
    def holdLeft(self):
        self._click('hold_left')
        
    def holdRight(self):
        self._click('hold_right')
        
    def holdMiddle(self):
        self._click('hold_middle')
        
    def releaseLeft(self):
        self._click('release_left')
        
    def releaseRight(self):
        self._click('release_right')
        
    def releaseMiddle(self):
        self._click('release_middle')

    def _mouseWheel(self, amt):
        """[Internal] Send <amt> 'clicks' to the OS to simulate
           movement of the mouse wheel."""
           
        #Unsure of how to test this - GUI movement is a large part
        #of the project, so I better figure it out.

        self._click('wheel', amt*self.wheelDelta)

    def mouseWheelUp(self, amount):
        self._mouseWheel(amount)
        
    def mouseWheelDown(self, amount):
        self._mouseWheel(-amount)
    
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
