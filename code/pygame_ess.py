# This file is part of Cryptography GUI, licensed under the MIT License.
# Copyright (c) 2020 Benedict Woo Jun Kai
# See LICENSE.md for more details.


######################################
# Import and initialize the librarys #
######################################
import logging
import pygame
import glob
import os
import traceback
import textwrap
from config import config


##################
# Initialization #
##################
logging.info('Loading pygame essentials classes...')
pygame.init()
screen = pygame.display.set_mode(config.screen_res())


########################
# Essentials functions #
########################
class pygame_ess:
    '''Essentials classes, functions and variables for pygame'''

    #############################
    # Shared / common variables #
    #############################
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # Common defined colours
    class colour:
        '''Common colour types in RGB tuple form'''
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        gray = (43, 43, 43)
        whiteish = (213, 213, 213)
    
    ###############
    # Create events #
    ###############
    class create:
        '''Creating for pygame shapes and surfaces'''

        def surface(size:tuple = (1024, 768), background_fill:tuple = None, is_alpha:bool = False): # -> pygame.surface.Surface:
            '''Create a new surface'''

            # Create window based on if is alpha
            if is_alpha: window = pygame.surface.Surface(size, pygame.SRCALPHA)
            else: window = pygame.surface.Surface(size)

            # set background color
            if background_fill != None: window.fill(background_fill)

            return window


    ###############
    # Load events #
    ###############
    class load:
        '''Loading of images and objects to surfaces'''

        def images(image_page:list, file_type:str = '.png', is_alpha:bool = False) -> dict:
            '''Load all images in a given directory to pygame surface'''

            # Define variables
            images = dict()
            image_dir = 'images/{}/'.format('/'.join(image_page))

            # If in code directory and not root, go back a step
            if os.path.basename(os.getcwd()) == 'code': image_dir = '../' + image_dir
            
            # Get all image file from givent directory
            image_dir_list = glob.glob(image_dir+"*"+file_type)

            # Warn on empty dir
            if len(image_dir_list) == 0: logging.error('No image found in {}'.format(image_dir))

            # Load them into pygame
            for image in image_dir_list:
                image_name = image.split('/')[-1].split('\\')[-1].split('.')[0]
                images[image_name] = pygame.image.load(image).convert_alpha() if is_alpha else pygame.image.load(image).convert()
                images[image_name] = pygame.transform.smoothscale(images[image_name], (int(images[image_name].get_width()*config.scale_w()), int(images[image_name].get_height()*config.scale_w())))

            return images

        def text(surface, object) -> pygame.surface.Surface:
            '''Load text of object, includes things liek text warping, align and multi line support'''

            # Grap text_data
            text_data = object.meta

            # Warp text if specified
            if text_data.warp_text != None:
                warpped_text = textwrap.wrap(text_data.text, width=text_data.warp_text)

                for line in range(len(warpped_text)):
                    if text_data.align == 'left': warpped_text[line] = '{1:<{0}}'.format(text_data.warp_text, warpped_text[line]).rstrip()
                    elif text_data.align == 'center': warpped_text[line] = '{1:^{0}}'.format(text_data.warp_text, warpped_text[line]).rstrip()
                    elif text_data.align == 'right': warpped_text[line] = '{1:>{0}}'.format(text_data.warp_text, warpped_text[line]).rstrip()
                    else: logging.error('Invalid alignment type {}'.format(text_data.align))

            # No text wrapping defined
            else: warpped_text = [text_data.text]

            # Generate surface for text
            text_surface = pygame_ess.create.surface(object.frame.box_size(), is_alpha=True)

            # Render multi line text
            h = 0
            for line in warpped_text:
                line_text = pygame.font.Font(text_data.font_type, text_data.font_size)
                rendered_text = line_text.render(line, True, text_data.colour)
                text_surface.blit(rendered_text, (0, h))
                h += line_text.size(line)[1]

            # Load to surface
            surface.blit(text_surface, (object.frame.box_coord()))

            return text_surface

        def object(surface, object, state:str = '', load_text:bool = True) -> None:
            '''Load an object to a pygame surface'''
            
            surface.blit(object.images[object.type+state], (object.frame.image_coord()))

            # Load text of object is a textfield
            if object.type == 'textfield': pygame_ess.load.text(surface, object)

        def objects(surface, objects:dict, names:list) -> None:
            '''Load mutliple objects to a pygame surface'''

            # Loop through object specified and load them
            for name in names:
                # Try to load object specified
                try: pygame_ess.load.object(surface, objects[name])
                # Error loading object
                except: logging.error('{} object not in objects dictionary.'.format(name))

        def surface(surface, window) -> None:
            '''Load a surface onto another pygame surface'''
            surface.blit(window.surface, window.frame.box_coord())

        def screen(surface, objects:dict) -> None:
            '''Load all objects given to screen'''

            # Load objects to window
            for object in objects.values():
                # Load image of item
                pygame_ess.load.object(surface, object)


    ##################
    # Display events #
    ##################
    class display:
        '''Display text, objects and surfaces to screen'''
        
        def object(window, object, state:str = '', direct_to_screen:bool = False) -> None:
            '''Display an object to screen'''

            if direct_to_screen: 
                screen.blit(object.images[object.type+state], (object.frame.image_coord()))
                pygame_ess.update()
            
            else: 
                pygame_ess.load.object(window.surface, object, state)
                pygame_ess.display.screen(window)

        def objects(window, objects:dict, names:list, direct_to_screen:bool = False) -> None:
            '''Display mutliple objects to screen'''

            # Draw direct to screen
            if direct_to_screen:
                # Loop through object specified and load them
                for name in names:
                    # Try to load object specified
                    try: screen.blit(objects[name].images[objects[name].type], (objects[name].frame.image_coord()))
                    # Error loading object
                    except: logging.error('[{}] {} object not in objects dictionary.'.format(window.name, name))
                
                pygame_ess.update()

            # Load objects to surface, then display to screen
            else:
                pygame_ess.load.objects(window.surface, objects, names)
                pygame_ess.display.screen(window)

        def surface(window, window_to_merge):
            '''Display a surface given to screen'''

            pygame_ess.load.surface(window.surface, window_to_merge)
            pygame_ess.display.screen(window)

        def screen(window, update_all:bool = False, objects:dict = None) -> None:
            '''Display all objects given to screen'''

            # Update all objects of the surface
            if update_all: pygame_ess.load.screen(window.surface, objects)

            # Ouput window to screen
            screen.blit(window.surface, (window.frame.bx, window.frame.by))

            # Draw to screen
            pygame_ess.update()


    #####################
    # Interaction event #
    #####################
    class event:
        '''Process actios by the user'''

        def selection(window, selection_objects:dict, direct_to_screen:bool = False) -> dict:
            '''Check for mouse hover and selections'''

            selection_result = {'object_name':'', 'object_type':'', 'action_result':''}

            for selection_object in selection_objects.values():
                # Skip selection check if runclass is empty
                if selection_object.runclass != None: 

                    # Check if mouse in selection object box
                    mouse_hover_over_object  = False
                    while selection_object.in_box(pygame.mouse.get_pos(), window.frame.box_coord()):
                        # Change to hover type
                        if selection_object.hover_action and not mouse_hover_over_object:
                            # Draws hover to surface
                            pygame_ess.display.object(window, selection_object, '_hover', direct_to_screen)
                            mouse_hover_over_object = True
                            logging.debug('[{}] Hovered on {} {}'.format(window.name, selection_object.name, selection_object.type))

                        # Run click event
                        click_result = pygame_ess.event.click(window, selection_object, selection_objects) 

                        # If clicked on object
                        if click_result != False: 
                            # Remove mouse hover
                            if mouse_hover_over_object: pygame_ess.load.object(window.surface, selection_object, '', direct_to_screen)
                            
                            # Load back previous screen
                            if click_result == True: 
                                pygame_ess.display.screen(window)
                                logging.info('loaded {}.'.format(window.name))

                            # Stores click_result
                            selection_result['object_name'] = selection_object.name
                            selection_result['object_type'] = selection_object.type
                            selection_result['action_result'] = click_result

                            # Return data of click result
                            logging.info('[{}] object_name:{}, object_type:{}, action_result:{}'.format(window.name, selection_result['object_name'], selection_result['object_type'], selection_result['action_result']))
                            return selection_result

                    # Moved out of hitbox
                    if mouse_hover_over_object: pygame_ess.display.object(window, selection_object, '', direct_to_screen)  

            # No selections/clicks were made
            return selection_result

        def click(window, selection_object, selection_objects) -> any:
            '''Check if mouse click on objects, and run defined actions'''

            for event in pygame.event.get():                
                # Check for left click
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    logging.info('[{}] Clicked on {} {}'.format(window.name, selection_object.name, selection_object.type))

                    # When there is no function to run
                    if type(selection_object.runclass) == str: return selection_object.runclass

                    # Load new screen
                    try: 
                        # Use selection_object as parameter
                        if selection_object.runclass_parameter == True: return selection_object.runclass(window, selection_object)
                        # No parameter needed
                        elif selection_object.runclass_parameter == False: return selection_object.runclass()
                        # Use custom parameter
                        else: return selection_object.runclass(selection_object.runclass_parameter)
                    
                    # When errors loading screen/runclass
                    except: 
                        logging.error('error running {} runclass.'.format(selection_object.runclass))
                        traceback.print_exc()
                        return True

                # When press closed windows
                if event.type == pygame.QUIT: return 'quit'

                # Check for other events
                pygame_ess.event.scroll(window, event)
                pygame_ess.event.keyboard(selection_objects, event)

            # User did not click
            return False  

        def keyboard(selection_objects, event):
            pass

        def scroll(window, event) -> None:
            '''Scrolling of surface'''

            # Check if scrolling is needed
            if config.screen.height - window.frame.h < 0 and window.scroll:
                # Check of scroll action
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Scroll up
                    if event.button == 4:
                        window.frame.by = min(window.frame.by + 35, 0)
                        pygame_ess.display.screen(window)
                        logging.debug('[{}] scrolled up {}'.format(window.name, window.frame.by))

                    # Scroll down
                    elif event.button == 5:
                        window.frame.by = max(window.frame.by - 35, min(config.screen.height - window.frame.h, 0))
                        pygame_ess.display.screen(window)
                        logging.debug('[{}] scrolled down {}'.format(window.name, window.frame.by))


    ########################
    # Other core functions #
    ########################
    def set_caption(caption:str = 'pygame time!'):
        '''Set window header title'''
        pygame.display.set_caption(caption)
        logging.debug('window captions set to {}'.format(caption))

    def update(tick:int = 60):
        '''Draw display changes to screen'''
        pygame.display.flip()
        pygame.display.update()
        pygame.time.Clock().tick(tick)

    def buffer(window) -> bool:
        '''Loop through pygame events and check of quit and scrolling'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return True
            pygame_ess.event.scroll(window, event)

    def quit():
        '''Exit from program'''
        logging.info('Exiting program...')
        pygame.quit()