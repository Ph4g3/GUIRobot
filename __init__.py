import os
import sys

directory = 'C:/Users/Ph4g3/workspace/GUIRobot/'

if os.path.isdir(directory):
    sys.path.append(directory)
    from Source import *
    from Test import *
    