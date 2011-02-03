#=========================#
#                         #
#     Version: 0.3        #
#  Author:  Martin Moore  #
#                         #
#=========================#

#Standard Modules
import ctypes
import ctypes.wintypes
import unittest
import os
import sys
import time

#Local modules
import Source.Virtual_HID as Virtual_HID        
        
class test_VMouse(unittest.TestCase):
    
    def setUp(self):
        """Create a fast virtual mouse"""
        
        self.mouse = Virtual_HID.VMouse(clickSpeed = 0)
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
        
        #Test for high/low edge cases for coordinates
        #i.e. greater than largest coordinate available.
        
        #NOTE: Maximum coords in windows is one less than resolution
        #e.g. max coords for 1920x1080 resolution is [1919, 1079]
        #Most likely to keep 1px of mouse cursor on screen
        resolution = ctypes.windll.user32.GetSystemMetrics(0), \
                     ctypes.windll.user32.GetSystemMetrics(1)
        self.mouse.setCoord(1000000, 1000000)
        ctypes.windll.user32.GetCursorPos(ctypes.byref(self.pt))
        self.assertEquals(resolution[0] - 1, self.pt.x)
        self.assertEquals(resolution[1] - 1, self.pt.y)
        
        #Illegal coordinates should default to 0, 0
        self.mouse.setCoord(-10, -10)
        ctypes.windll.user32.GetCursorPos(ctypes.byref(self.pt))
        self.assertEquals(0, self.pt.x)
        self.assertEquals(0, self.pt.y)        
        
    def test_click(self):
        self.mouse.setCoord(500, 500)
        time.sleep(0.5)
        
        #Virtual key codes to check state of
        #a given key. Note: Different codes used for
        #clicking/releasing keys. Damn MS.
        vKeyCodes = [0x01, 0x02, 0x08]
        clickValues = ['hold_left', 'hold_right', 'hold_middle']
        releaseValues = ['release_left', 'release_right', 'release_middle']
        
        try:
            i = 0
            for value in clickValues:
                self.mouse._click(value)
                self.assertTrue(self.getKeyState(vKeyCodes[i]))
                self.mouse._click(releaseValues[i])
                i += 1
        except AssertionError:
            print(sys.exc_info()[1])
        finally:
            #Release everything regardless of test results
            for value in releaseValues:
                self.mouse._click(value)
            
            
    def getKeyState(self, vKeyCode):
        state = bin(ctypes.windll.user32.GetKeyState(vKeyCode))
        state = state.split('b')[1]
        if state[0] == '1':
            return True
        else:
            return False
     
def main():
    """Run tests."""
    suite = unittest.TestLoader().loadTestsFromTestCase(test_VMouse)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
if __name__ == '__main__':
    main()    
