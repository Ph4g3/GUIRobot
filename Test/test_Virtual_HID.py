import ctypes
import ctypes.wintypes
import unittest
import threading

import os
import sys

import time

directory = 'C:/Users/Ph4g3/workspace/GUIRobot/'

if os.path.isdir(directory):
    sys.path.append(directory)
    from Source.Virtual_HID import *
    
#class KeyStateListener(threading.Thread):
#    """A class used to listen for button presses."""
#    
#    def __init__(self, vKeyCode, timeToListen):
#        threading.Thread.__init__(self)
#        self.vKeyCode = vKeyCode
#        self.timeToListen = timeToListen
#        self.keyState = False
#    
#    def run(self):
#        startTime = time.time()
#        while time.time() < startTime + self.timeToListen:
#            if self.checkState():
#                self.setKeyState(True)
#                break
#            
#    def checkState(self):
#        """State is in binary form. High order bit shows whether key
#           is up or down (0 or 1 respectively). Low order bit shows
#           whether key is toggled on or off (0 or 1 respectively)."""
#           
#        state = bin(ctypes.windll.user32.GetKeyState(self.vKeyCode))
#        state = state.split('b')[1]
#        if state[0] == '1':
#            return True
#        return False
#    
#    def getKeyState(self):
#        return self.keyState
#    
#    def setKeyState(self, state):
#        self.keyState = state
        
        
class test_VMouse(unittest.TestCase):
    
    def setUp(self):
        """Create a fast virtual mouse"""
        
        self.mouse = VMouse(clickSpeed = 0)
        self.pt = ctypes.wintypes.POINT()
        
    def tearDown(self):
        """Force python to clean up."""
        
        del self.mouse
        del self.pt
        
    def test_getCoord(self):
        ctypes.windll.user32.SetCursorPos(100, 100)
        self.pt = self.mouse.getCoord()
        self.assertEquals(100, self.pt.x)
        self.assertEquals(100, self.pt.y)
        
    def test_setCoord(self):
        self.mouse.setCoord(100, 100)
        ctypes.windll.user32.GetCursorPos(ctypes.byref(self.pt))
        self.assertEquals(100, self.pt.x)
        self.assertEquals(100, self.pt.y)
        
    def test_click(self):
        self.mouse.setCoord(455, 455)
        time.sleep(0.5)
        
        #Virtual key codes to check state of
        #a given key. Note: Different codes used for
        #clicking/releasing keys.
        vKeyCodes = [0x01, 0x02, 0x04]
        clickValues = [0x02, 0x08, 0x20]
        releaseValues = [0x04, 0x10, 0x40]
        
        i = 0
        for clickValue in clickValues:
            try:
                self.mouse._click([clickValue])
            finally:
                self.assertTrue(self.getKeyState(vKeyCodes[i]))
                self.mouse._click([releaseValues[i]])
            i += 1
            
    def getKeyState(self, vKeyCode):
        state = bin(ctypes.windll.user32.GetKeyState(vKeyCode))
        state = state.split('b')[1]
        if state[0] == '1':
            return True
        return False
        
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_VMouse)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
