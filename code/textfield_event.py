# This file is part of Cryptography GUI, licensed under the MIT License.
# Copyright (c) 2020 Benedict Woo Jun Kai
# See LICENSE.md for more details.


######################################
# Import and initialize the librarys #
######################################
import logging
import pygame
import time
from pygame_ess import pygame_ess



#################################################
# Handles textfield objects and keyboard input #
#################################################
class textfield_event:
    '''Handles textfield objects and keyboard input'''

    def update_textfield(window, textfield_object, backspace=False):
        '''Update the text displayed on screen'''
        
        # textfield is selected, add a _ and load selected background
        if not backspace: 
            pygame_ess.display.object(window, textfield_object, '_selected')
            textfield_object.meta.text += '_'
            pygame_ess.display.object(window, textfield_object, '_selected')
            textfield_object.meta.text = textfield_object.meta.text[:-1]
        
        # textfield is selected but backspace is pressed
        else: pygame_ess.display.object(window, textfield_object, '_selected')

    
    def exit_textfield(window, textfield_object):
        # Check if input is valid
        if textfield_object.meta.validation == None or textfield_object.meta.validation.check(textfield_object.meta.text):
            # Exit from texfield if so
            pygame_ess.display.object(window, textfield_object)
            logging.info('Exited {} textfield.'.format(textfield_object.name))
            return True

        # Load back screen
        pygame_ess.display.screen(window)
        return False


    def run(window, textfield_object) -> str:
        '''keyboard input'''

        # Check if there is input validation
        if textfield_object.meta.validation == None: logging.warn('No input validation specified.')

        textfield_event.update_textfield(window, textfield_object)
        logging.info('Loaded '+textfield_object.name+' textfield.')

        # Key repeat variables
        key_pressed = []
        time_pressed, repeat_interval = 0, 1.2

        while True:
            for event in pygame.event.get():
                # if keyboard is pressed
                if event.type == pygame.KEYDOWN:

                    # Exit textfield if click return or escape
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        # Exit textfield
                        if textfield_event.exit_textfield(window, textfield_object): return textfield_object.meta.text

                    # Allow only based on validation defined
                    elif event.key in textfield_object.meta.validation.chars_allowed: key_pressed.append(event)

                # Key is released
                elif event.type == pygame.KEYUP:
                    # reset key variables
                    # Variables
                    for pressed in range(len(key_pressed)):
                        if key_pressed[pressed].key == event.key:
                            key_pressed.pop(pressed)
                            time_pressed, repeat_interval = 0, 1.2
                            break

                # Exit textfield if click out
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Check clicked outside of textfield
                    if not textfield_object.in_box(pygame.mouse.get_pos(), window.frame.box_coord()):
                        # Exit textfield
                        if textfield_event.exit_textfield(window, textfield_object): return textfield_object.meta.text

                # Quit program
                elif event.type == pygame.QUIT: return 'quit'

                # check for Scroll
                pygame_ess.event.scroll(window, event)

            # Apply keypress, key repeat based on repeat interval in seconds
            if key_pressed != [] and time.time() - time_pressed >= repeat_interval:

                new_text = textfield_object.meta.text

                # remove character
                if key_pressed[-1].key == pygame.K_BACKSPACE: new_text = textfield_object.meta.text[:-1]
                    
                # Add character
                else: new_text += key_pressed[-1].unicode

                # Do not exceed max length
                if textfield_object.meta.validation == None or len(new_text) <= textfield_object.meta.validation.max_length:
                    # Stores the new_text
                    textfield_object.meta.text = new_text
                    # Update textfield
                    textfield_event.update_textfield(window, textfield_object)

                # Setup for next key repeat
                time_pressed = time.time()
                if repeat_interval > 0.025: repeat_interval /= 4
