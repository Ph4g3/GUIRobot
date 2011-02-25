#=========================#
#                         #
#     Version: 0.4        #
#  Author:  Martin Moore  #
#                         #
#=========================#

#Standard Modules
import ctypes
import ctypes.wintypes
import unittest
import time
import logging

from subprocess import Popen

#Local modules
import GUIRobot.Source.Virtual_HID as Virtual_HID        

testLog = logging.getLogger('GUIRobot.Test.test_Virtual_HID')

class test_VKeyboard(unittest.TestCase):
    
    def setUp(self):
        """Create a fast virtual keyboard with a text editor to
           recieve input"""
           
        testLog.debug('====Keyboard testing started====')
        
        self.strings = ['this is a lower case string',
                        'This is a Mixed Case String',
                        """/,.\#';[]-""",
                        #Cannot support pound symbol atm.
                        """!"%^&*()_+"""]
        
        #Create a file for writing to
        self.testFile = 'C:/vKeybd.txt'
        file = open(self.testFile)
        file.close()
        
        self.commandString = """VK_CAPSLOCK this string should be in caps VK_CAPSLOCK"""
        self.commandResult = """THIS STRING SHOULD BE IN CAPS"""
        self.resolution = ctypes.windll.user32.GetSystemMetrics(0), \
                          ctypes.windll.user32.GetSystemMetrics(1)
        self.notepad = self.openEditor()
        self.showWindow()
        self.keyboard = Virtual_HID.VKeyboard()
        
        self.writeStrings()

    def tearDown(self):
        self.closeEditor(self.notepad)
        del self.keyboard
        
    def writeStrings(self):
        for string in self.strings:
            self.keyboard.type(string)
        self.keyboard.type(self.commandString)
    
    def openEditor(self):
        app = Popen('notepad.exe', self.testFile)
        return app
        
    def closeEditor(self, app):
        try:
            app.kill()
        except:
            print("Can't close the application.")
        
    def showWindow(self, windowTitle='Untitled - Notepad'):
        """Attempts to find a window name "windowTitle" and show it
           maximized"""
           
        h = ctypes.wintypes.HWND
        ctypes.windll.user32.FindWindowA.restype = ctypes.wintypes.POINTER(h)
        h = ctypes.windll.user32.FindWindowA(None, 'Untitled - Notepad')
        return ctypes.windll.user32.ShowWindow(h, 3)
            
#    def test_stringsFromFile(self):
#        pass
        

class test_VMouse(unittest.TestCase):
    
    def setUp(self):
        """Create a fast virtual mouse"""
        
        testLog.debug('====Mouse testing started====')
        
        self.mouse = Virtual_HID.VMouse(clickSpeed = 0.2)
        self.pt = ctypes.wintypes.POINT()
        
    def tearDown(self):
        """Force python to clean up."""
        
        testLog.debug('====Mouse testing finished====')
        
        del self.mouse
        del self.pt
        
    def test_getCoord(self):
        ctypes.windll.user32.SetCursorPos(100, 100)
        self.pt = self.mouse.getCoords()
        self.assertEquals(100, self.pt.x)
        self.assertEquals(100, self.pt.y)
        
    def test_setCoords(self):
        self.mouse.setCoords(100, 100)
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
        self.mouse.setCoords(1000000, 1000000)
        ctypes.windll.user32.GetCursorPos(ctypes.byref(self.pt))
        self.assertEquals(resolution[0] - 1, self.pt.x)
        self.assertEquals(resolution[1] - 1, self.pt.y)
        
        #Illegal coordinates should default to 0, 0
        self.mouse.setCoords(-10, -10)
        ctypes.windll.user32.GetCursorPos(ctypes.byref(self.pt))
        self.assertEquals(0, self.pt.x)
        self.assertEquals(0, self.pt.y)        
        
    def test_click(self):
        
        #Virtual key codes to check state of
        #a given key. Note: Different codes used for
        #clicking/releasing keys. Damn MS.
        xCoord, yCoord = 500, 500
        vKeyCodes = [0x01, 0x02, 0x04]
        clickValues = ['hold_left', 'hold_right', 'hold_middle']
        releaseValues = ['release_left', 'release_right', 'release_middle']
        
        #Get current state of mouse - buttons are stored in toggled
        #states regardless of whether they are off or on.
        states = []
        for x in vKeyCodes:
            states.append(ctypes.windll.user32.GetKeyState(x))
        
        try:
            i = 0
            for value in clickValues:
                self.mouse.setCoords(xCoord, yCoord)
                self.mouse._click(value)
                self.assertTrue(self.getKeyState(vKeyCodes[i], states[i]), msg=clickValues[i]+
                                ' '+releaseValues[i])
                self.mouse._click(releaseValues[i])
                i += 1
                
        finally:
            #Release everything regardless of test results
            for value in releaseValues:
                self.mouse._click(value)
            
    #Duplicate function, should be made into module method:
    #Source.Virtual_HID.getKeyState()      
    def getKeyState(self, vKeyCode, oldState):
        state = bin(ctypes.windll.user32.GetKeyState(vKeyCode))
        testLog.debug(str(vKeyCode)+' returned '+state)
        state = state.split('b')[1]
        if state[0] != oldState:
            return True
        else:
            return False
     
def main():
    """Run tests."""
    suite =  unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_VKeyboard))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_VMouse))
    
    unittest.TextTestRunner(verbosity=2).run(suite)
            
if __name__ == '__main__':
    main()    
