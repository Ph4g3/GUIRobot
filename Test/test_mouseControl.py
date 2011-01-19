import mouseControl
import unittest
import ctypes

class test_movement(unittest.TestCase):

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
        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_movement)
    unittest.TextTestRunner(verbosity=2).run(suite)
