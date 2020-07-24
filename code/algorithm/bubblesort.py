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


class bubblesort:

    @staticmethod
    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data

        # Reset stats
        sort_screen.objects.time_taken.data.startTimer(withReset=True)
        sort_screen.objects.moves.data.reset()

        for counter in range(array.bars-1, -1, -1):
            # Compare each pair
            didSwap = False
            index = -1
            for index in range(counter):
                # Add a move
                sort_screen.objects.moves.data.moved()
                
                # Set bars to selected colour
                array.barslist[index].state('selected')
                array.barslist[index+1].state('selected')
                sort_screen.objects.sortbox.display()

                action_result = commonFunc.waitAction(sort_screen, speed/2)
                if action_result != None: return action_result

                # Swap the bars
                if array.barslist[index+1].number < array.barslist[index].number:
                    action_result = array.swap(index, index+1, speed)
                    if action_result != None: return action_result
                    didSwap = True

                # Unselect the bars
                array.barslist[index].state()

                action_result = commonFunc.waitAction(sort_screen, speed/2)
                if action_result != None: return action_result
            
            # Unselect the bars
            array.barslist[index+1].state()

            # If all pairs are sorted
            if not didSwap: break

            action_result = commonFunc.waitAction(sort_screen, speed/2)
            if action_result != None: return action_result

        # Sort is completed
        sort_screen.objects.time_taken.data.stopTimer()
        action_result = array.completed()
        if action_result != None: return action_result