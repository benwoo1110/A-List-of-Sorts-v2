######################################
# Import and initialize the librarys #
######################################
import time
from pygame_objects import *


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

    # Allow A-Z and all 
    chars_allowed = list(range(32,65)) + list(range(91,127)) + [8]

    def run(screen, itemName):

        # Keyboard
        key_pressed, time_pressed, repeat_interval = [], 0, 1.2

        # Get textfield item
        textfield_item = screen.objects[itemName]
        textfield_item.load()

        while True:
            # Get check for interaction with screen
            action_result = textfield_screen.event.action()

            # No action
            if action_result == None: continue

            # When program is set to close
            if action_result.contains('outcome','__quit__'): return '__quit__'

            # Going back
            if action_result.contains('outcome', 'go_back'): return '__back__' 

            # When keyboard is pressed
            if action_result.didAction('keyboard'):
                # Key is pressed
                if action_result.keyboard.isType('keydown') and action_result.keyboard.name in textfield.chars_allowed:
                    key_pressed.append(action_result.keyboard.name)

                # Key is released
                elif action_result.keyboard.isType('keyup') and action_result.keyboard.name in key_pressed:
                    key_pressed.remove(action_result.keyboard.name)
                    # Reset variables
                    time_pressed, repeat_interval = 0, 1.2

            # Engage key
            if key_pressed != [] and time.time() - time_pressed >= repeat_interval:

                new_text = textfield_item.data.text

                # remove character
                if key_pressed[-1] == pygame.K_BACKSPACE: new_text = textfield_item.data.text[:-1]
                    
                # Add character
                else: new_text += chr(key_pressed[-1])

                # Stores the new_text
                textfield_item.data.text = new_text
                # Update textfield
                textfield_item.display()

                # Setup for next key repeat
                time_pressed = time.time()
                if repeat_interval > 0.025: repeat_interval /= 4