######################################
# Import and initialize the librarys #
######################################
import time
from pygame_objects import *


class bubblesort:

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

                select_time = time.time()
                while time.time() - select_time < speed/2: 
                    sort_screen.objects.time_taken.data.updateTimer()
                    sort_screen.event.action()

                # Swap the bars
                if array.barslist[index+1].number < array.barslist[index].number:
                    array.swap(index, index+1, speed)
                    didSwap = True

                # Unselect the bars
                array.barslist[index].state()

                select_time = time.time()
                while time.time() - select_time < speed/2:
                    sort_screen.objects.time_taken.data.updateTimer()
                    sort_screen.event.action()
            
            # Unselect the bars
            array.barslist[index+1].state()

            # If all pairs are sorted
            if not didSwap: break

            select_time = time.time()
            while time.time() - select_time < speed/2:
                sort_screen.objects.time_taken.data.updateTimer()
                sort_screen.event.action()

        # Sort is completed
        sort_screen.objects.time_taken.data.stopTimer()
        array.completed()