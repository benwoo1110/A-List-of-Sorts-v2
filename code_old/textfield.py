######################################
# Import and initialize the librarys #
######################################
import time
from code.pygame_objects import *


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


textfield_screen = screen(
    name = 'textfield',
    keyboardParameters = {
        'back': {
            'keys': {13, 27},
            'runclass': runclass(action='go_back')
        }
    }
)



class textfield:

    @staticmethod
    def run(text_screen, itemName):
        # Set surface
        textfield_screen.surface = text_screen.surface

        # Get textfield item
        textfield_item = text_screen.objects[itemName]
        textfield_item.switchState('Selected')

        time_pressed, repeat_interval = 0, 1.2

        while True:

            pressed_key = None

            for char in keypressed:
                if textfield_item.data.validateChar(char.key): 
                    pressed_key = char

            # Engage key
            if pressed_key != None and time.time() - time_pressed >= repeat_interval:

                # remove character
                if pressed_key.key == 8: 
                    textfield_item.data.setText(textfield_item.data.text[:-1])
                    
                # Add character
                else: textfield_item.data.setText(textfield_item.data.text + pressed_key.unicode)

                # Setup for next key repeat
                time_pressed = time.time()
                if repeat_interval > 0.025: repeat_interval /= 3

            # Get check for interaction with screen
            action_result = textfield_screen.event.action()

            # No action
            if action_result == None: continue
            # When program is set to close
            if action_result.contains('outcome','__quit__'): return '__quit__'
            # Going back
            if action_result.contains('outcome', 'go_back'): 
                textfield_item.data.validateText()
                return '__back__' 

            # Reset repeat timing on key release
            if action_result.didAction('keydown'): pass
                 
            if action_result.didAction('keyup'): 
                if textfield_item.data.validateChar(char.key): time_pressed, repeat_interval = 0, 1.2