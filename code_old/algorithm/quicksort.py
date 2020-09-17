######################################
# Import and initialize the librarys #
######################################
import time
from code.algorithm.commonFunc import commonFunc
from code.pygame_objects import *


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


class quicksort:

    @staticmethod
    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data
        
        # Reset stats
        sort_screen.objects.time_taken.data.startTimer(withReset=True)
        sort_screen.objects.moves.data.reset()