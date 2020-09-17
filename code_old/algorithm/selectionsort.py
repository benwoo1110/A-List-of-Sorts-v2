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


class selectionsort:

    @staticmethod
    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data
        
        # Reset stats
        sort_screen.objects.time_taken.data.startTimer(withReset=True)
        sort_screen.objects.moves.data.reset()

        # Loop through all the bar index
        for index in range(array.bars):

            # Check for the lowest number
            lowest_index = index
            for check in range(index, array.bars):
                # Add a move
                sort_screen.objects.moves.data.moved()

                # Number is lower than the current lowest
                if array.barslist[check].number < array.barslist[lowest_index].number:
                    array.barslist[lowest_index].state()
                    lowest_index = check
                    array.barslist[check].colour = pg_ess.colour.green

                    sort_screen.objects.sortbox.display()

                    action_result = commonFunc.waitAction(sort_screen, speed/2)
                    if action_result != None: return action_result

                # Just show selected if not
                else:
                    array.barslist[check].state('selected')
 
                    sort_screen.objects.sortbox.display()

                    action_result = commonFunc.waitAction(sort_screen, speed/2)
                    if action_result != None: return action_result
                                        
                    array.barslist[check].state()

            action_result = array.move(lowest_index, index, speed)
            if action_result != None: return action_result

            array.barslist[index].state('done')

        # Sort is completed
        sort_screen.objects.time_taken.data.stopTimer()
        action_result = array.completed()
        if action_result != None: return action_result
