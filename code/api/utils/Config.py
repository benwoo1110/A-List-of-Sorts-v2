######################################
# Import and initialize the librarys #
######################################
import yaml
import os
import traceback
import time


###########################
# Loading config to class #
###########################
class Struct:
    def __init__(self, **response):
        for key,value in response.items():
            if isinstance(value, dict): setattr(self, key, Struct(**value))
            else: setattr(self, key, value)

    def __repr__(self): return '{}'.format(self.__dict__)


##################
# Config actions #
##################
class Config:
    default_file_dir = './gamefiles/default_config.yml'
    file_dir = './config.yml'

    @staticmethod
    def check():
        # Create file if it doesnt exist
        if not os.path.isfile(Config.file_dir):
            with open(Config.default_file_dir, 'r') as default_config_file:
                default_config_contents = default_config_file.read()

            with open(Config.file_dir, 'w') as config_file:
                config_file.write(default_config_contents)
                print("Generated new default config at ./config.yml")

    @staticmethod
    def get() -> Struct:
        try:
            # Read from config file
            with open(Config.file_dir) as config_file:
                parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
                config_file.close()

        except FileNotFoundError: 
            # File not found, run check to create new one
            print('Config not found, trying to create a new one...')
            Config.check()

            # Try again
            with open(Config.file_dir) as config_file:
                parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
                config_file.close()

        except:
            traceback.print_exc()
            # Possible issue with yaml file formating, try reset config
            print('Config seem broken, renaming it to ./config_broken.yml')
            os.rename(Config.file_dir, f'./config_broken_{time.time()}.yml')
            Config.check()

            # Try again
            with open(Config.file_dir) as config_file:
                parsed_config_file = yaml.load(config_file, Loader=yaml.FullLoader)
                config_file.close()

        # Load config dict to a structured class
        return Struct(**parsed_config_file)


###################
# Checking config #
###################
Config.check()
