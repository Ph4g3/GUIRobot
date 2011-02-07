import os
import sys

"""This is the package which contains all modules relevant to the project.
   All it contains is a directory to my workspace to make it easier to work
   with eclipse."""

directory = 'C:/Users/Ph4g3/workspace/GUIRobot/'
if os.path.isdir(directory):
    sys.path.append(directory)