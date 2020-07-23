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
# Get configuration #
#####################
# Set to code directory
sys.path.insert(1, './code')
# Import config options
from config import config


#################################
# Starting Cryptography GUI app #
#################################
if __name__ == "__main__":
    # Get home screen
    from home import *

    # Run home screen
    pg_ess.core.caption('A List of Sorts v2')
    home.run()

    # End program
    pg_ess.core.quit()