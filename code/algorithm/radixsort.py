######################################
# Import and initialize the librarys #
######################################
import time
from pygame_objects import *



class selectionsort:

    @staticmethod
    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data
        
        # Reset stats
        sort_screen.objects.time_taken.data.startTimer(withReset=True)
        sort_screen.objects.moves.data.reset()