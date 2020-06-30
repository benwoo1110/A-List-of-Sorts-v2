# This file is part of Cryptography GUI, licensed under the MIT License.
# Copyright (c) 2020 Benedict Woo Jun Kai
# See LICENSE.md for more details.


######################################
# Import and initialize the librarys #
######################################
import sys
import os
import pkg_resources
import logging
import logging.handlers
from datetime import datetime


##########################
# Check for dependencies #
##########################
print('Checking depencencies...')

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


#####################
# Get configuration #
#####################
# Set to code directory
sys.path.insert(1, './code')
# Import config options
from config import config


#######################
# Setup debug logging #
#######################

# Ensure that logs folder is created
if not os.path.isdir('./logs'):
    # Create logs directory
    try: os.mkdir('logs')
    except OSError: print("[ERROR] Creation of the directory ./logs failed")
    else: print("[INFO] Successfully created the directory ./logs")

# Get date
# datetime object containing current date and time
now = datetime.now()
# Convert to file dir
log_file_dir = now.strftime("./logs/%d-%m-%Y_%H-%M-%S_debug.log")

# Change root logger level from WARNING (default) to NOTSET in order for all messages to be delegated.
logging.getLogger().setLevel(logging.NOTSET)

# Add stdout handler, with level INFO
console = logging.StreamHandler(sys.stdout)
console.setLevel(level=os.environ.get("LOGLEVEL", config.debug_level.console))
formater = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
console.setFormatter(formater)
logging.getLogger().addHandler(console)

# Add file debug handler, with level DEBUG
debugHandler = logging.handlers.RotatingFileHandler(filename=log_file_dir, mode='w')
debugHandler.setLevel(level=os.environ.get("LOGLEVEL", config.debug_level.logs))
formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
debugHandler.setFormatter(formatter)
logging.getLogger().addHandler(debugHandler)


#################################
# Starting Cryptography GUI app #
#################################
if __name__ == "__main__":
    logging.info('Starting Crpytography GUI...')
    logging.info(config)

    # Initialize pygame
    from pygame_oop import pg_ess
    from home import home

    # Run home screen
    pg_ess.core.set_caption('Cryptography GUI')

    # End program
    pg_ess.core.pygame_ess.quit()