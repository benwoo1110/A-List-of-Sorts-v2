# This file is part of Cryptography GUI, licensed under the MIT License.
# Copyright (c) 2020 Benedict Woo Jun Kai
# See LICENSE.md for more details.


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

        # Dependencies is all good
        else: print('{} is installed.'.format(dependency))


#################################
# Starting Cryptography GUI app #
#################################
if __name__ == "__main__":

    # Initialize pygame
    from pygame_oop import pg_ess
    from home import home

    # Run home screen
    pg_ess.core.set_caption('Cryptography GUI')

    # End program
    pg_ess.core.pygame_ess.quit()