######################################
# Import and initialize the librarys #
######################################
import time
from pygame_core import *


class textfield:

    chars_allowed = list(range(32,65)) + list(range(91,127)) + [8]

    def run(screen, itemName):
        # Get textfield item
        textfield_item = screen.objects[itemName]

        # Key repeat variables
        key_pressed = []
        time_pressed, repeat_interval = 0, 1.2

        textfield_item.load()

        while True:
            for event in pygame.event.get():
                # if keyboard is pressed
                if event.type == pygame.KEYDOWN:

                    # Exit textfield if click return or escape
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        # Exit textfield
                        textfield_item.switchState('')
                        return 'edited'
                    
                    # Add to list of keys taht are pressed
                    if event.key in textfield.chars_allowed: key_pressed.append(event)

                # Key is released
                elif event.type == pygame.KEYUP:
                    # reset key variables
                    for pressed in range(len(key_pressed)):
                        if key_pressed[pressed].key == event.key:
                            key_pressed.pop(pressed)
                            time_pressed, repeat_interval = 0, 1.2
                            break

                # Exit textfield if click out
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check clicked outside of textfield
                    if not textfield_item.frame.box.mouseIn(screen.surface.frame.coord()):
                        # Exit textfield
                        textfield_item.switchState('')
                        return 'edited'

                # Quit program
                if screen.event.quit(event) == '__quit__': return '__quit__'

                # check for Scroll
                screen.event.scroll(event)

            # Apply keypress, key repeat based on repeat interval in seconds
            if key_pressed != [] and time.time() - time_pressed >= repeat_interval:

                new_text = textfield_item.data.text

                # remove character
                if key_pressed[-1].key == pygame.K_BACKSPACE: new_text = textfield_item.data.text[:-1]
                    
                # Add character
                else: new_text += key_pressed[-1].unicode

                # Stores the new_text
                textfield_item.data.text = new_text
                # Update textfield
                textfield_item.display()

                # Setup for next key repeat
                time_pressed = time.time()
                if repeat_interval > 0.025: repeat_interval /= 4
