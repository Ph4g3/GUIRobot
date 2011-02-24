#=========================#
#                         #
#     Version: 0.5        #
#  Author:  Martin Moore  #
#                         #
#=========================#

import time
import logging
import threading
import ctypes

from ctypes.wintypes import (c_int, c_long, c_short, c_byte, c_ulong, c_ushort, 
                             POINT, POINTER, Structure, Union, sizeof, HHOOK,
                             HINSTANCE)

#Start logger.
VHIDLog = logging.getLogger('GUIRobot.Source.VHID')
VHIDLog.debug('Virtual_HID module initialized.')

##############################################################################
## TEST SECTION - TO BE REMOVED ##############################################
##############################################################################
#class KeyBdLogger(threading.Thread):
#    """Key logger for keyboard events."""
#    
#    def __init__(self):
#        threading.Thread.__init__(self)
#        self.KeyBdHook = HHook()
#        self.messages = []
#        self.id = threading.current_thread().ident
#        #print type(self.id), self.id
#        
#    def run(self):
#        #Print 2 seconds of vkCodes
#        start = time.time()
#        while time.time() < (start + 2):
#            self.KeyBdHook.hook = self.SetWindowsHookEx(13, self.KeyboardProc,
#                                                        self.GetModuleHandle(0), 0)
#            if self.KeyBdHook.hook == 0:
#                print 'ERROR: '+str(ctypes.windll.kernel32.GetLastError())
#        
##            print type(self.KeyBdHook.hook)
##            print self.KeyBdHook.hook
#                #Unhook our shit regardless of outcome
#            self.UnhookWindowsHookEx(self.KeyBdHook.hook)
#            
#        print self.messages
#                
#    def KeyboardProc(self, nCode, wParam, lParam):
#        """LLKeyboard procedure callback function for our hook to the OS.
#        
#           nCode tells us if we should pass an event onto the actual recipient 
#           of the message first. We'll ignore this for now as we want to record
#           all keystrokes.
#           
#           wParam gives us info on whether the key was pressed or released.
#           
#           lParam is a pointer to our KBLLSTRUCT.
#           
#           http://msdn.microsoft.com/en-us/library/ms644985(v=vs.85).aspx"""
#          
#        #nCode tells us if we should pass an event onto the actual recipient of the
#        #message first. I say screw that - I want all the keystrokes first.
#        if nCode < c_int(0):
##            Keyboard event is passed through lParam, so copy this into our Python
##            KBDLLStruct type using a windows function 'MoveMemory'
#
#           
#            #Because it's a windows function calling this method, we'll want to
#            #pass back information that we've taken so it can be used by other applications.
#            return ctypes.windll.user32.GetNextHookEx(self.KeyBdHook.hook,
#                                                  nCode, wParam, lParam)
#        else:
#            ctypes.windll.kernel32.RtlMoveMemory(ctypes.addressof(self.KeyBdHook.kStruct),
#                                                 ctypes.c_void_p(lParam),
#                                                 ctypes.sizeof(lParam))
#            
#            self.message.append(self.KeyBdHook.kStruct)
#        
#    def SetWindowsHookEx(self, idHook, lpFn, hMod, dwThreadId):
#        """Cast our python types into a Windows function type"""
#        WinFunc = ctypes.WINFUNCTYPE(c_ulong, c_ulong, c_ulong, c_ulong, c_ulong)
#        return ctypes.windll.user32.SetWindowsHookExA(idHook, WinFunc(lpFn), hMod, dwThreadId)
#    
#    def GetModuleHandle(self, lpModuleName):
#        return ctypes.windll.kernel32.GetModuleHandleA(lpModuleName)
#    
#    def UnhookWindowsHookEx(self, hHook):
#        return ctypes.windll.user32.UnhookWindowsHookEx(hHook)
#    
#class HHook():
#    """A handle for the hook we use to get keyboard keystrokes."""
#    
#    def __init__(self):
#        self.hook = HHOOK
#        self.kStruct = KBLLHOOKSTRUCT()
#
#class KBLLHOOKSTRUCT(Structure):
#    """Holds information about keyboard events we receive from a hook procedure.
#       Keyboard Low Level Hook Structure.
#       http://msdn.microsoft.com/en-us/library/ms644967(v=vs.85).aspx"""
#    
#    #Kind of annoying how similar this is to the KeyBdInput Struct.
#    _fields_ = [("vkCode", c_ulong),
#                ("scanCode", c_ulong),
#                ("flags", c_ulong),
#                ("time", c_ulong),
#                ("dwExtraInfo", POINTER(c_ulong))]
##############################################################################
            
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
             ("dwExtraInfo", POINTER(c_ulong))]

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
             ("dwExtraInfo", POINTER(c_ulong))]

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
       
    def __init__(self, typeSpeed = 0.05):
        """Init of our VKeyboard sets up an ulong for
           extra information provided by the operating system,
           an Input Interface object and the virtual key code
           table."""
        
        self.initState = self._getKeyboardState()
        
        #Zero all the keys of the keyboard
        zeroState = KeyBdState()
        for button in zeroState.array:
            button = 0
        self._setKeyboardState(zeroState)
            
        self.extra = c_ulong(0)
        self.click = Input_I()
        self.typeSpeed = typeSpeed
        
        self.specials = """-=+[];'#\,./"""
        
        #Modified 3 is a pound symbol, but seems to be misinterpreted by python.
        #Damn them brits.
        self.modSpecials = {
        '!': 1,    '"': 2,   '$': 4,
        '%': 5,    '^': 6,   '&': 7,   '*': 8,
        '(': 9,    ')': 0,   '_': '-', '{': '[',
        '}': '}',  ':': ';', '@': "'", '~': '#',
        '|': '\\', '<': ',', '>': '.', '?': '/'
        }

        self.vKeyTable = { 'VK_BACKSPACE': 0x08,
                           'VK_TAB': 0x09,
                           'VK_ENTER': 0x0D,
                           'VK_SHIFT': 0x10,
                           'VK_CTRL': 0x11,
                           'VK_ALT': 0x12,
                           'VK_PAUSE': 0x13,
                           'VK_CAPSLOCK': 0x14,
                           'VK_ESCAPE': 0x1B,
                           ' ': 0x20,
                           'VK_SPACEBAR': 0x20,
                           'VK_PAGEUP': 0x21,
                           'VK_PAGEDOWN': 0x22,
                           'VK_END': 0x23,
                           'VK_HOME': 0x24,
                           'VK_LEFT': 0x25,
                           'VK_UP': 0x26,
                           'VK_RIGHT': 0x27,
                           'VK_DOWN': 0x28,
                           'VK_PRINTSCR': 0x2C,
                           'VK_INSERT': 0x2D,
                           'VK_DELETE': 0x2E,
                           'VK_HELP': 0x2F,
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
                           'a': 0x41,
                           'b': 0x42,
                           'c': 0x43,
                           'd': 0x44,
                           'e': 0x45,
                           'f': 0x46,
                           'g': 0x47,
                           'h': 0x48,
                           'i': 0x49,
                           'j': 0x4a,
                           'k': 0x4b,
                           'l': 0x4c,
                           'm': 0x4d,
                           'n': 0x4e,
                           'o': 0x4f,
                           'p': 0x50,
                           'q': 0x51,
                           'r': 0x52,
                           's': 0x53,
                           't': 0x54,
                           'u': 0x55,
                           'v': 0x56,
                           'w': 0x57,
                           'x': 0x58,
                           'y': 0x59,
                           'z': 0x5a,
                           'VK_LWINKEY': 0x5B,
                           'VK_RWINKEY': 0x5C,
                           'VK_APPKEY': 0x5D,
                           'VK_SLEEP': 0x5F,
                           'VK_NUM0': 0x60,
                           'VK_NUM1': 0x61,
                           'VK_NUM2': 0x62,
                           'VK_NUM3': 0x63,
                           'VK_NUM4': 0x64,
                           'VK_NUM5': 0x65,
                           'VK_NUM6': 0x66,
                           'VK_NUM7': 0x67,
                           'VK_NUM8': 0x68,
                           'VK_NUM9': 0x69,
                           'VK_MULTIPLY': 0x6A,
                           'VK_ADD': 0x6B,
                           #What the hell is the Separator key?
                           'VK_SEP': 0x6C,
                           'VK_SUB': 0x6D,
                           'VK_DECIMAL': 0x6E,
                           'VK_DIVIDE': 0x6E,
                           'VK_F1': 0x70,
                           'VK_F2': 0x71,
                           'VK_F3': 0x72,
                           'VK_F4': 0x73,
                           'VK_F5': 0x74,
                           'VK_F6': 0x75,
                           'VK_F7': 0x76,
                           'VK_F8': 0x77,
                           'VK_F9': 0x78,
                           'VK_F10': 0x79,
                           'VK_F11': 0x7a,
                           'VK_F12': 0x7b,
                           'VK_F13': 0x7c,
                           'VK_F14': 0x7d,
                           'VK_F15': 0x7e,
                           'VK_F16': 0x7f,
                           'VK_F17': 0x80,
                           'VK_F18': 0x81,
                           'VK_F19': 0x82,
                           'VK_F20': 0x83,
                           'VK_F21': 0x84,
                           'VK_F22': 0x85,
                           'VK_F23': 0x86,
                           'VK_F24': 0x87,
                           'VK_NUMLOCK': 0x90,
                           'VK_SCROLL': 0x91,
                           'VK_LSHIFT': 0xA0,
                           'VK_RSHIFT': 0xA1,
                           'VK_LCTRL': 0xA2,
                           'VK_RCTRL': 0xA3,
                           'VK_LMENU': 0xA4,
                           'VK_RMENU': 0xA5,

                           #Browser Buttons
                           'VK_B_Back': 0xA6,
                           'VK_B_Forward': 0xA7,
                           'VK_B_Refresh': 0xA8,
                           'VK_B_Stop': 0xA9,
                           'VK_B_Search': 0xAA,
                           'VK_B_Favorites': 0xAB,

                           'VK_VOL_MUTE': 0xAD,
                           'VK_VOL_DOWN': 0xAE,
                           'VK_VOL_UP': 0xAF,
                           'VK_NEXT_TRACK': 0xB0,
                           'VK_PREV_TRACK': 0xB1,
                           'VK_STOP_TRACK': 0xB2,
                           'VK_PLAY_PAUSE': 0xB3,
                           'VK_MAIL': 0xB4,
                           'VK_MEDIA': 0xB5,
                           'VK_APP1': 0xB6,
                           'VK_APP2': 0xB7,
                           
                           #Misc key, varies by keyboard
                           ';': 0xBA,
                           'VK_SEMI_COLON': 0xBA,
                           
                           '+': 0xBB,
                           'VK_OEM_PLUS': 0xBB,
                           
                           ',': 0xBC,
                           'VK_OEM_COMMA': 0xBC,
                           
                           '-': 0xBD,
                           'VK_OEM_MINUS': 0xBD,
                           
                           '.': 0xBE,
                           'VK_OEM_PERIOD': 0xBE,
                           
                           #Misc key, varies by keyboard
                           '/': 0xBF,
                           'VK_SLASH': 0xBF,
                           
                           #Misc key, varies by keyboard
                           "'": 0xC0,
                           'VK_APOSTROPHE': 0xC0,
                           
                           #Misc key, varies by keyboard
                           '[': 0xDB,
                           'VK_OPEN_SQUARE_BRACKET': 0xDB,
                           
                           #Misc key, varies by keyboard
                           '\\': 0xDC,
                           'VK_BACKSLASH': 0xDC,
                           
                           #Misc key, varies by keyboard
                           ']': 0xDD,
                           'VK_CLOSE_SQUARE_BRACKET': 0xDD,
                           
                           #Misc key, varies by keyboard
                           '#': 0xDE,
                           'VK_HASH': 0xDE,
                        }
        #Might be helpful
        #http://www.kbdedit.com/manual/low_level_vk_list.html
        
        VHIDLog.debug('Virtual keyboard instantiated.')
                           
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
            item = ': '+str(items.next()[0]).rjust(14, '.')
            state = ': '+self._getKeyState(kState.array[i])
            
            #Concatenate all strings and store in list
            states.append(strValue+item+state)
            i+=1
        states.sort()
        for buttonState in states:
            print buttonState
    
    def _input(self, key, dwFlags=0,):
        """[Internal] Takes a virtual key code and sends it to
           the operating system. By default this pushes a button.
           dwFlags=0x02 to release a button"""

        self.click.ki = KeyBdInput(key, 0, dwFlags, 0, ctypes.pointer(self.extra))
        x = Input(1, self.click)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        time.sleep(self.typeSpeed)
        
    def _parse(self, string):
        
        """Parses strings into representations of virtual codes, which are
           eventually turned into actual hex key codes. Every "vKey" is in 
           a list of it's own for characters that need modifiers. e.g.:
               a = 'a' = _input(0x41)
               A = 'VK_SHIFT' + 'a' = _input(0x10); _input(0x41)"""
    
        vKeys = []
        words = string.split(' ')
        #Add spaces taken out by str.split()
        i = 1
        for spaces in range(len(words)-1):
            words.insert(i, ' ')
            i+=2
    
        for word in words:
            if word is ' ':
                vKeys.append([word])
            elif word.startswith('VK_'):
                #Assume it's in vKeyTable, should try-except this
                vKeys.append([word])
            else:
                for letter in word:
                    if letter.isupper():
                        vKeys.append(['VK_LSHIFT', letter.lower()])
                    elif letter.isalpha():
                        vKeys.append([letter])
                    elif letter.isdigit():
                        vKeys.append([int(letter)])
                    elif letter in self.specials:
                        vKeys.append([letter])
                    elif letter in self.modSpecials:
                        vKeys.append(['VK_LSHIFT', self.modSpecials[letter]])
                        
        return vKeys
        
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
        

    def _translateKey(self, key):
        """[Internal]Translate a virtual key code into an actual 'keyboard
           key'."""
           
        if self.vKeyTable.has_key(key):
            return self.vKeyTable.get(key)
        else:
            print key, " is not valid"
#            raise ValueError('Error on key %s' %key)

    def type(self, string):
        """Takes a normal user string, such as this docstring, parses it, 
           converts it and simulates user input via the keyboard. """
        
        VHIDLog.debug('Typing: '+string)
        vKeys = self._parse(string)                
        self._keyAction(*vKeys)
        
    def _keyAction(self, *args):
        """[Internal] Simulates a key press and release."""
        
        for action in args:
            for vKey in action:
                keyCode = self._translateKey(vKey)
                self._input(keyCode)
                #Release the keys that were just pressed.
            for vKey in action:
                keyCode = self._translateKey(vKey)
                self._input(keyCode, dwFlags=2)
            
            
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
        
        VHIDLog.debug('Virtual mouse instantiated.')
        
    def getCoords(self):
        """Gets the current mouse coordinates from the OS.
           Returns a POINT object."""
           
        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt

    def setCoords(self, xCoord, yCoord):
        """Pass coordinates to the OS to set the mouse at
           the desired coordinates."""
           
        ctypes.windll.user32.SetCursorPos(xCoord, yCoord)
        
        VHIDLog.debug('Mouse coordinates set at '+str(xCoord)+', '+str(yCoord))
        
    def setPointCoords(self, point):
        """Pass coordinates to the OS to set the mouse at
           the desired point."""
           
        if type(point) is POINT:
            self.setCoords(point.x, point.y)
        else:
            raise TypeError

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
            
        VHIDLog.debug(clickType+" mouse button clicked.")
            
    def _translateClick(self, buttonToClick):
        """[Internal] Translate our click type to virtual key codes 
           representing a click and release tuple."""
           
        if self.clickTable.has_key(buttonToClick):
            return self.clickTable.get(buttonToClick)
        else:
            raise ValueError

    def leftClick(self):
        """Performs a left click and releases it."""
        
        self._click('left')

    def rightClick(self):
        """Performs a right click and releases it."""
        
        self._click('right')

    def middleClick(self):
        """Performs a middle click and releases it."""
        
        self._click('middle')
        
    def holdLeft(self):
        """Holds down left mouse button until released with with releaseLeft()."""

        self._click('hold_left')
        
    def holdRight(self):
        """Holds down right mouse button until released with with releaseRight()."""

        self._click('hold_right')
        
    def holdMiddle(self):
        """Holds down middle mouse button until released with with releaseMiddle()."""

        self._click('hold_middle')
        
    def releaseLeft(self):
        """Releases left click. """
               
        self._click('release_left')
        
    def releaseRight(self):
        """Releases right click. """
        
        self._click('release_right')
        
    def releaseMiddle(self):
        """Releases middle click."""
        
        self._click('release_middle')

    def _mouseWheel(self, amt):
        """[Internal] Send <amt> 'clicks' to the OS to simulate
           movement of the mouse wheel."""
           
        #Unsure of how to test this - GUI movement is a large part
        #of the project, so I better figure it out.

        self._click('wheel', amt*self.wheelDelta)

    def mouseWheelUp(self, amount):
        """Moves mouse wheel one 'click' away from the user."""
        
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
