######################################
# Import and initialize the librarys #
######################################
import logging
import sys
import os
import pkg_resources


##########################
# Check for dependencies #
##########################
with open('requirements.txt', 'r') as requirements:
    # Getting dependencies list needed
    dependencies = requirements.read().split('\n')

    for dependency in dependencies:
        # Check if dependencies meets the requirements
        try: pkg_resources.require(dependency)

        # If dependencies out of date
        except pkg_resources.VersionConflict:
            print('Dependency {} outdated. Attempting to update now...'.format(dependency))
            os.system('pip3 install --no-cache-dir {}'.format(dependency))

        # If dependencies is not found/installed.
        except pkg_resources.DistributionNotFound:
            print('Dependency {} not found. Attempting to install now...'.format(dependency))
            os.system('pip3 install --no-cache-dir {}'.format(dependency))


#####################
# Import code stuff #
#####################
from code.config import config
from code.pygame_core import *
from code.home import home


#################################
# Starting Cryptography GUI app #
#################################
home.run()

# End program
logger.info('Exiting program... Goodbye!')
pygame.quit()