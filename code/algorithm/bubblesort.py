######################################
# Import and initialize the librarys #
######################################
import time
from pygame_objects import *


class bubblesort:

    def run(sort_screen, speed:int):
        count = 1
        array = sort_screen.objects.sortbox.data
        sort_screen.objects.time_taken.data.startTimer(withReset=True)

        while True:
            # Compare each pair
            didSwap = False
            for index in range(array.bars - count):
                array.barslist[index].state('selected')
                array.barslist[index+1].state('selected')
                sort_screen.objects.sortbox.display()

                select_time = time.time()
                while time.time() - select_time < speed/2: 
                    sort_screen.objects.time_taken.data.updateTimer()
                    sort_screen.event.action()

                if array.barslist[index+1].number < array.barslist[index].number:
                    array.swap(index, index+1, speed)
                    didSwap = True

                array.barslist[index].state()

                select_time = time.time()
                while time.time() - select_time < speed/2:
                    sort_screen.objects.time_taken.data.updateTimer()
                    sort_screen.event.action()

            count += 1
            
            array.barslist[index+1].state()

            # If all pairs are sorted
            if not didSwap: break

        sort_screen.objects.time_taken.data.stopTimer()
        array.completed()
        