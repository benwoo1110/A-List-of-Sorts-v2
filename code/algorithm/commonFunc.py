######################################
# Import and initialize the librarys #
######################################
import time


class commonFunc:

    @staticmethod
    def waitAction(sort_screen, speed:float):
        select_time = time.time()
        while time.time() - select_time < speed: 
            sort_screen.objects.time_taken.data.updateTimer()
            action_result = commonFunc.getAction(sort_screen)
            if action_result != None: return action_result
            
    @staticmethod
    def getAction(sort_screen):
        action_result = sort_screen.event.action()

        # No action
        if action_result == None: return
        # When program is set to close
        if action_result.contains('outcome','__quit__'): return '__quit__'
        # Going back
        if action_result.contains('outcome', 'go_back'): return '__back__' 
        # Load back screen
        if action_result.contains('outcome', '__back__'): sort_screen.surface.display(withLoad=False)