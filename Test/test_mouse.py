import mouseControl
from   InputActions import *
import unittest
import ctypes

class mouseControlTestCase(unittest.TestCase):

    def setUp(self):
        #Initialize SUT
        self.m = mouseControl.mouseControl()

    def tearDown(self):
        del self.m

    def test_compareFloatToInt(self):
        self.assertTrue(self.m.compareFloatToInt(12.75, 13))
        self.assertTrue(self.m.compareFloatToInt(13.0, 13))
        self.assertFalse(self.m.compareFloatToInt(12.0, 13))
        self.assertTrue(self.m.compareFloatToInt(12.74, 12))

    def test_grabPoint(self):
        ctypes.windll.user32.SetCursorPos(100, 100)
        
        grabbedPoint = self.m.grabPoint()
        
        self.assertEquals(100, grabbedPoint.x)
        self.assertEquals(100, grabbedPoint.y)

    def test_moveCursor(self, moveInterval = 0.0001):
        #Movement trajectory: diagonal right and down.
        xCoords = range(500)
        yCoords = range(500)
        
        #Use the moveCursor() function
        self.m.moveCursor(xCoords, yCoords, moveInterval)

        #Get the last point
        grabbedPoint = self.m.grabPoint()

        #Check if we are at the last point pair in our coords lists.
        self.assertEquals(xCoords[len(xCoords)-1], grabbedPoint.x)
        self.assertEquals(yCoords[len(yCoords)-1], grabbedPoint.y)

    #def test_checkMoving(self):
        #Threading can probably be used to test this
        

class mouseActionsTestCase(unittest.TestCase):

    def setUp(self):
        self.m = mouseActions()
        self.buttonToTest = 'right'

    def tearDown(self):
        del self.m, self.buttonToTest

    def test_doClick(self):
        #Set up left click and check mouse state
        self.m.doClick(self.buttonToTest)
        short = self.getButtonStateShort()
        self.assertEquals(short[0], '1')

        #Regardless of outcome, send a left button release
        extra = c_ulong(0)
        click = Input_I()
        click.mi = MouseInput(0, 0, 0, 0x04, 0, pointer(extra))
        x = Input(0, click)
        windll.user32.SendInput(1, pointer(x), sizeof(x))
        
    def test_releaseClick(self):
        #Use the mouseActions class to do a click and then release it
        self.m.doClick(self.buttonToTest)
        self.m.releaseClick()

        #Now we must check if the mouse is in the correct state
        short = self.getButtonStateShort()
        self.assertEquals(short[0], '0')

    def test_getButtonStates(self):
        #Ensure that no buttons are pressed on mouse
        self.m.releaseClick()
        clickedButtons = self.m.getButtonStates()
        for x in clickedButtons:
            self.assertEquals(x, False)

    def test_sendInput(self):
        temp = self.buttonToTest.lower()
        if temp == 'left':
            button = 2
        elif temp == 'right':
            button = 8
        elif temp == 'middle':
            button = 64

        self.m.sendInput(button)
        short = self.getButtonStateShort()

        #self.assertEquals(short[0], '1')
        self.m.releaseClick()

    def test_getClickValue(self):
        buttonStrs = ['left', 'middle', 'right']
        expectedReturns = [2, 8, 32]

        i = 0
        for x in buttonStrs:
            self.assertTrue(self.m.getClickValue(x), \
                            expectedReturns[i])

    def getButtonStateShort(self):
        button = self.buttonToTest.lower()
        
        if button == 'left':
            state = 0x01
        elif button == 'right':
            state = 0x02
        elif button == 'middle':
            state = 0x04

        if state:
            buttonState = ctypes.windll.user32.GetKeyState(state)
            short = bin(buttonState)[len(bin(buttonState))-16:]
            return short

        return None

if __name__ == '__main__':
    suite1 = unittest.TestLoader().loadTestsFromTestCase(mouseControlTestCase)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(mouseActionsTestCase)

    suite = unittest.TestSuite([suite1, suite2])
    unittest.TextTestRunner(verbosity=2).run(suite)

    print("If you have encountered errors, it is likely that test cases which",
          "have passed are not reliable. Resolve earlier errors first and rerun")
