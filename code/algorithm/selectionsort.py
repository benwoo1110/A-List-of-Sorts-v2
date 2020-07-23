######################################
# Import and initialize the librarys #
######################################
import time


class selectionsort:

    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data

        # Loop through all the bar index
        for index in range(array.bars):

            # Check for the lowest number
            lowest_index = index
            for check in range(index, array.bars):
                if array.barslist[check].number < array.barslist[lowest_index].number:
                    array.barslist[lowest_index].state()
                    lowest_index = check
                    array.barslist[check].colour = (136, 250, 78)

                    sort_screen.objects.sortbox.display()

                    select_time = time.time()
                    while time.time() - select_time < speed/2: action_result = sort_screen.event.action()

                else:
                    array.barslist[check].state('selected')
 
                    sort_screen.objects.sortbox.display()

                    select_time = time.time()
                    while time.time() - select_time < speed/2: action_result = sort_screen.event.action()
                    
                    array.barslist[check].state()

            array.move(lowest_index, index, speed)

        array.completed()
