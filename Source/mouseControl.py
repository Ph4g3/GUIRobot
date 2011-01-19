import time
import ctypes
import ctypes.wintypes

from InputActions import mouseActions

# Mouse click information here:
# http://kvance.livejournal.com/985732.html
# Try implementing this.

class mouseControl():
    
    def getCursorPoints(self, moveInterval = 0.1, samples = -1, consolePrinting = True):
        """
        Records cursor movement in 0.1 second intervals.
        Returns two arrays: xCoords, yCoords
        """

        if consolePrinting:
            if samples != -1:
                print("Recording cursor movement for", moveInterval*samples, \
                      "seconds, in intervals of", moveInterval, "seconds")
            else:
                print("Recording cursor movement in", moveInterval, \
                      "seconds increments. Press Ctrl-C to stop")
        
        xCoords = []
        yCoords = []

        while samples:
            try:
                while True:
                    pt = self.grabPoint()
                    xCoords.append(pt.x)
                    yCoords.append(pt.y)
                    if samples == -1:
                        pass
                    else:
                        samples -= 1
                        if not samples:
                            break
                    time.sleep(moveInterval)
            except KeyboardInterrupt:
                break
            finally:
                return xCoords, yCoords

    def grabPoint(self):
        pt = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        return pt
        

    def moveCursor(self, xCoords, yCoords, moveInterval = 0.1):
        """
        Given a list of x coordinates and y coordinates,
        move the mouse in moveInterval increments (default
        == 0.1)
        """

        i = 0
        for x in xCoords:
            ctypes.windll.user32.SetCursorPos(xCoords[i], yCoords[i])
            time.sleep(moveInterval)
            i += 1

    def checkMoving(self, timeToWait, moveInterval = 0.1):
        """
        Given a timeToWait value, we poll the mouse coordinates
        to see if the cursor is moving. If it moves, return True,
        otherwise wait for timeToWait to elapse and return False.
        """
        
        xCoords = []
        yCoords = []

        elapsedTimeEst = 0
        countDownTime = timeToWait

        done = False

        while not done:
            #Use the following line to countdown timeToWait
            #Need to abstract the int checking below for this
            #to work well.
            timeLeft = timeToWait - elapsedTimeEst

            if self.compareFloatToInt(float(timeLeft), countDownTime):
                print("Stopping in " + str(countDownTime) + "...")
                countDownTime -= 1

            pt = self.grabPoint()
            if len(xCoords) > 1:
                if xCoords[len(xCoords)-1] != xCoords[len(xCoords)-2] or \
                   yCoords[len(yCoords)-1] != yCoords[len(yCoords)-2]:
                    return True
            xCoords.append(pt.x)
            yCoords.append(pt.y)
            time.sleep(moveInterval)
            elapsedTimeEst += moveInterval

            if self.compareFloatToInt(elapsedTimeEst, timeToWait):
                done = True
                
        i = 0
        #Use this list to mark points as equal
        samePoints = []
        for point in range(len(xCoords)-1):
            if xCoords[i] == xCoords[i+1] and \
               yCoords[i] == yCoords[i+1]:
                samePoints.append(True)
            else:
                samePoints.append(False)
            i += 1

        #If our samePoints list is filled with 'True' values
        #then our points are all the same and we're not moving.
        #return False. Otherwise, we've moved. return True.
        if samePoints.count(True) == len(samePoints):
            return False

        return True

    def compareFloatToInt(self, aFloat, anInt):
        """
        Use rounding to check if a float is
        the same as an integer. Not terribly accurate,
        but it'll do.
        """

        strFloat = str(aFloat)
        strFloat = strFloat.split('.')

        #if our float is x.75, round up,
        #otherwise, round down.
        if strFloat[1] >= str(75):
            aFloat = round(aFloat)
        else:
            aFloat = int(strFloat[0])

        if aFloat == anInt:
            return True
        
        return False

    def recordCursorAndPlayback(self, timeToWait):
        """
        Records a series of cursor movements until it
        stops for the specified time. Then we can proceed
        with playback.
        """
        
        xCoords = []
        yCoords = []
        while self.checkMoving(timeToWait):
            coordTuple = self.getCursorPoints(samples = 10, consolePrinting=True)
            xCoords.append(coordTuple[0])
            yCoords.append(coordTuple[1])

        print("Cursor stopped.")

        if len(xCoords) != 0 and len(yCoords) != 0:
            raw_input('Press enter to replay action')
            
        i = 0
        for x in xCoords:
            self.moveCursor(xCoords[i], yCoords[i])
            i += 1

        print("Playback complete")

