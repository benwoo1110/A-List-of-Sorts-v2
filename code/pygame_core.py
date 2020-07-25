######################################
# Import and initialize the librarys #
######################################
import logging
import os
import sys
import glob
import traceback
from datetime import datetime
from code.config import config


##############
# Get config #
##############
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
config = config.Config


###########
# Logging #
###########
# Ensure that logs folder is created
if not os.path.isdir('./logs'):
    # Create logs directory
    try: os.mkdir('logs')
    except: traceback.print_stack()
    else: print("Created ./logs directory")

# Keep only certain number of log files 
log_files = glob.glob("./logs/*.log")

for index in range(len(log_files) - max(0, config.logging.keep_logs-1)): #log_files[:min(-1, -config.logging.keep_logs)]:
    os.remove(log_files[index])

# setup log format and location
FORMATTER = logging.Formatter('[%(asctime)s %(levelname)s] [%(name)s] %(message)s', datefmt='%H:%M:%S')
LOG_FILE = datetime.now().strftime("./logs/%d-%m-%Y_%H-%M-%S.log")

class log:
    @staticmethod
    def get_console_handler():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level=os.environ.get("LOGLEVEL", config.logging.console_level.upper()))
        console_handler.setFormatter(FORMATTER)
        return console_handler

    @staticmethod
    def get_file_handler():
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setLevel(level=os.environ.get("LOGLEVEL", config.logging.file_level.upper()))
        file_handler.setFormatter(FORMATTER)
        return file_handler

    @staticmethod
    def get_logger(logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(log.get_console_handler())
        logger.addHandler(log.get_file_handler())
        return logger


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))
logger.debug('[config] {}'.format(config))


#####################
# Initialise screen #
#####################
import pygame
pygame.init()
window = pygame.display.set_mode(config.screen_res())


#####################
# Core parent class #
#####################
class coreFunc:
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __repr__(self): return '{}'.format(self.__dict__)


######################
# Essentials Classes #
######################
class pg_ess:

    ##########################
    # Common defined colours #
    ##########################
    class font:
        '''fonts found in fonts folder'''
        futura = './fonts/Futura.ttc'


    ##########################
    # Common defined colours #
    ##########################
    class colour:
        '''Common colour types in RGB tuple form'''
        black = (0, 0, 0)
        white = (255, 255, 255)
        gray = (43, 43, 43)
        whiteish = (213, 213, 213)
        orange = (255, 143, 8)
        selected = (150, 150, 150)
        red = (255, 100, 78)
        green = (136, 250, 78)
        lightgreen = (200, 255, 200)
    

    ##################
    # Core functions #
    ##################
    class core:
        @staticmethod
        def caption(caption:str = 'pygame time!'):
            pygame.display.set_caption(caption)
            logger.info('Set window title to "{}"'.format(caption))
        
        @staticmethod
        def update(tick:int = config.ticks):
            pygame.display.flip()
            pygame.display.update()
            pygame.time.Clock().tick_busy_loop(tick)
        
        @staticmethod
        def buffer():
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pg_ess.core.quit()

        @staticmethod
        def quit():
            logger.info('Exiting program... Goodbye!')
            pygame.quit()
