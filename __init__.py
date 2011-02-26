import logging
import logging.config

"""This is the package which contains all modules relevant to the project."""

import os
import sys

#Add my own directory to sys.path so Python can find it
mydir = 'C:/Users/Ph4g3/workspace/'
if os.path.isdir(mydir):
    sys.path.append(mydir)
    directory = mydir
#Otherwise default location is in python27
else:
    directory = os.getcwd()

#Start our logging from file configuration
logging.config.fileConfig(directory+'/GUIRobot/logger.conf')
log = logging.getLogger('GUIRobot')
log.debug('Logging initialized.')