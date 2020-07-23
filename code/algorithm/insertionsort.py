######################################
# Import and initialize the librarys #
######################################
import time


class insertionsort:

    def run(sort_screen, speed:int):
        array = sort_screen.objects.sortbox.data

        # Loop through second bar onwards
        for index in range(1, array.bars):

            # Set colours for the curretn index bar
            array.barslist[index].state('selected')
            sort_screen.objects.sortbox.display()

            select_time = time.time()
            while time.time() - select_time < speed/2: action_result = sort_screen.event.action()

            # check if bar needs to move
            moveTo = index
            for check in range(index-1, -1, -1):
                if array.barslist[index].number >= array.barslist[check].number: break
                else: 
                    array.barslist[check].colour = (255, 100, 78)
                    moveTo = check

                    sort_screen.objects.sortbox.display()

                    select_time = time.time()
                    while time.time() - select_time < speed/2: action_result = sort_screen.event.action()

            # Bar needs to move pos
            if moveTo != index: array.move(index, moveTo, speed)

            select_time = time.time()
            while time.time() - select_time < speed/2: action_result = sort_screen.event.action()

            array.barslist[index].state()

        array.completed()