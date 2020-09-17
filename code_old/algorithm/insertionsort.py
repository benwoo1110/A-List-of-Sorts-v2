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


class insertionsort:

    @staticmethod
    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data
        
        # Reset stats
        sort_screen.objects.time_taken.data.startTimer(withReset=True)
        sort_screen.objects.moves.data.reset()

        # Loop through second bar onwards
        for index in range(1, array.bars):

            # Set colours for the curretn index bar
            array.barslist[index].state('selected')
            sort_screen.objects.sortbox.display()

            action_result = commonFunc.waitAction(sort_screen, speed/2)
            if action_result != None: return action_result

            # check if bar needs to move
            moveTo = index
            for check in range(index-1, -1, -1):
                # Add a move
                sort_screen.objects.moves.data.moved()

                # Check where should the bar move to
                if array.barslist[index].number >= array.barslist[check].number: break
                
                else: 
                    array.barslist[check].colour = pg_ess.colour.red
                    moveTo = check

                    sort_screen.objects.sortbox.display()

                    action_result = commonFunc.waitAction(sort_screen, speed/2)
                    if action_result != None: return action_result

            # Bar needs to move pos
            if moveTo != index: 
                action_result = array.move(index, moveTo, speed)
                if action_result != None: return action_result

            else:
                array.barslist[index].state('')

            action_result = commonFunc.waitAction(sort_screen, speed/2)
            if action_result != None: return action_result

        # Sort is completed
        sort_screen.objects.time_taken.data.stopTimer()
        action_result = array.completed()
        if action_result != None: return action_result