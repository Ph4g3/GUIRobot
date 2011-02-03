import os
import sys

"""This init module needs to be modified to be more robust
   i.e. find our project if it is not contained in my workspace"""

directory = 'C:/Users/Ph4g3/workspace/GUIRobot/'

#Perhaps os.walk will help us look through our GUIRobot directory,
#and get all relevant paths - i.e. add GUIRobot.Source, GUIRobot.Test
#to sys.path. Then can we initialize Virtual_HID.VMouse without needing
#to say GUIRobot.Source.Virtual_HID.VMouse()

if os.path.isdir(directory):
    sys.path.append(directory)
    try:
        import Source
        import Test
    except ImportError:
        print(sys.exc_info()[1])
else:
    print(directory+' is not a valid path.')
