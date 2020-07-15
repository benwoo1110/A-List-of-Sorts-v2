######################################
# Import and initialize the librarys #
######################################
import logging
import yaml
import os

##########################
# Getting configurations #
##########################

# Default setting for file
default_config_contents = '''\
###############################
# Cryptography GUI config.yml #
###############################

# NOTE: Change only if you know what you are doing!

# Size of pygame window in pixel
screen:
  width: 1024
  height: 768

# Level of output shown
# CRITICAL -> 50
# ERROR -> 40
# WARNING -> 30
# INFO -> 20
# DEBUG -> 10
debug_level:
  # For console output
  console: 'INFO'
  # App activities logged in './cryptography-GUI/logs'
  logs: 'DEBUG'

# Changes the refresh rate of pygame
ticks: 60

# Change speed of scrolling
scroll_speed: 35
'''

# Set config file directory
config_dir = './config.yml'
if os.path.basename(os.getcwd()) == 'code': config_dir = '../config.yml'

# Create file if it doesnt exist
if not os.path.isfile(config_dir):
    with open(config_dir, 'w') as config_file:
        config_file.write(default_config_contents)

# Read from config file
with open(config_dir) as config_file:
    parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
    config_file.close()


###########################
# Loading config to class #
###########################
class Struct:
    def __init__(self, **response):
        for k,v in response.items():
            if isinstance(v,dict):
                self.__dict__[k] = Struct(**v)
            else:
                self.__dict__[k] = v

    def screen_res(self) -> tuple:
        return (self.screen.width, self.screen.height)

    def scale_w(self) -> float:
        return (self.screen.width/1024)

    def scale_h(self) -> float:
        return (self.screen.height/768)

    def __str__(self):
        return '[config] {}'.format(parsed_config_file)

# Convert dict to class object
config = Struct(**parsed_config_file)


###############
# For testing #
###############
if __name__ == "__main__":
    print(config)