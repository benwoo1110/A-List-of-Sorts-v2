# This file is part of Cryptography GUI, licensed under the MIT License.
# Copyright (c) 2020 Benedict Woo Jun Kai
# See LICENSE.md for more details.


######################################
# Import and initialize the librarys #
######################################
import logging
import os
from pygame_ess import pygame_ess
from config import config

logging.info('Loading item storage classes...')


#######################################
# Storage images and its cooridinates #
#######################################
class coord:
    def __init__(self, bx:int = 0, by:int = 0, w:int = 0, h:int = 0, ix:int = 0, iy:int = 0, scale:bool = True):
        self.scale:bool = scale

        if scale:
            self.bx:int = int(bx * config.scale_w())
            self.by:int = int(by * config.scale_w())
            self.w:int = int(w * config.scale_w())
            self.h:int = int(h * config.scale_w())
            self.ix:int = int(ix * config.scale_w())
            self.iy:int = int(iy * config.scale_w())
        else:
            self.bx:int = int(bx)
            self.by:int = int(by)
            self.w:int = int(w)
            self.h:int = int(h)
            self.ix:int = int(ix)
            self.iy:int = int(iy)

    def box_size(self) -> tuple: 
        return (self.w, self.h)

    def box_coord(self, surface_coord:tuple = (0, 0)) -> tuple: 
        return (self.bx + surface_coord[0], self.by + surface_coord[1])
    
    def image_coord(self, surface_coord:tuple = (0, 0)) -> tuple: 
        return (self.ix + surface_coord[0], self.iy + surface_coord[1])

    def __str__(self):
        return 'bx:{} by:{} w:{} h:{} ix:{} iy:{} scale:{}'.format(self.bx, self.by, self.w, self.h, self.ix, self.iy, self.scale)


#####################################
# Stores data for text & textfields #
#####################################
class text_data:
    def __init__(self, text:str = '', font_type:str = None, calculate_font_dir:bool = True, font_size:int = 36, 
    warp_text:int = None, align:str = 'left', colour:set = (0, 0, 0), validation = None):
        self.text:str = text
        self.calculate_font_dir:bool = calculate_font_dir
        self.colour:tuple = colour
        self.validation = validation
        self.warp_text:int = warp_text
        self.align:str = align

        # Scale font size
        self.font_size:int = int(font_size * config.scale_w())

        # Get font file from fonts folder
        if calculate_font_dir:
            # Get font type file
            font_dir:str = 'font/'+font_type
            # If in code directory and not root, go back a step
            if os.path.basename(os.getcwd()) == 'code': font_dir = '../' + font_dir
            # Save dir of custom font
            self.font_type:str = font_dir
        
        # Save font_type directly
        else: self.font_type:str = font_type

    def __str__(self):
        return '''text:{}, warp_text:{}, align:{}
      font: (type:{}, size:{}, colour:{})
      validation:{}'''.format(self.text, self.warp_text, self.align, self.font_type, self.font_size, self.colour, self.validation)


###########################
# Storages UI object data #
###########################
class item:
    def __init__(self, name:str = 'name', type:str = 'object', meta:any = None, load_images:dict = None, images:dict = {},
    frame:coord = coord(), hover_action:bool = None, runclass:any = None, runclass_parameter:bool = None):
        # Stores object data
        self.name:str = name
        self.type:str = type
        self.meta:any = meta
        self.frame:coord = frame
        self.runclass:any = runclass

        # Ensure that textfield has teh correct meta
        if meta == None and self.type == 'textfield': 
            logging.warn('No text meta data defined for {} textfield, setting default text_data.'.format(self.name))
            self.meta = text_data()

        # Set to default hover_action if not defined
        if hover_action == None: self.hover_action:bool = self.type == 'button'
        else: self.hover_action:bool = hover_action

        # Set to default runclass_parameter if not defined
        if runclass_parameter == None: self.runclass_parameter = self.type == 'textfield'
        else: self.runclass_parameter:bool = runclass_parameter

        # Load images
        if load_images != None: self.images:dict = pygame_ess.load.images(**load_images)
        else: self.images:dict = images

        # Debug objects
        logging.debug(self.__str__())

    def in_box(self, mouse_pos:tuple, surface_coord:tuple = (0, 0)) -> bool:
        # Save surface coord to seperate variables
        scroll_x:int = surface_coord[0]
        scroll_y:int = surface_coord[1]
        # Return if in box
        return self.frame.bx + scroll_x < mouse_pos[0] < self.frame.bx + self.frame.w + scroll_x and self.frame.by + scroll_y < mouse_pos[1] < self.frame.by + self.frame.h + scroll_y

    def __str__(self):
        return '''
name:{}, type:{}, hover_action:{}
meta: {} 
images: {}
frame: {}
runclass:{}, runclass_parameter:{}'''.format(self.name, self.type, self.hover_action, self.meta, self.images, self.frame, self.runclass, self.runclass_parameter)


##########################
# Store suface of window #
##########################
class surface:
    def __init__(self, window_objects:dict, name:str = 'window', frame:coord = None, 
    background_fill:tuple = pygame_ess.colour.gray, load:bool = True, is_alpha:bool = False, scroll:bool = True):
       
        # Calculate smart height of window size if no frame defined
        if frame == None:
            logging.warn('No frame defined for surface {}, doing smart frame calculation.'.format(name))
            frame = coord(bx=0, by=0, w=1024, h=0, scale=False)
            for window_object in window_objects.values():
                frame.h = max(frame.h, window_object.frame.iy+window_object.frame.h)

        # Custom scale
        frame.bx = int(frame.bx * config.scale_w())
        frame.by = int(frame.by * config.scale_w())
        frame.w = int(frame.w * config.scale_w())
        if config.scale_h() < config.scale_w(): frame.h = int(frame.h * config.scale_w())
        else: frame.h = int(frame.h * config.scale_h())

        # Create the surface
        window = pygame_ess.create.surface(frame.box_size(), background_fill, is_alpha)

        # Load surface
        if load: pygame_ess.load.screen(window, window_objects)

        # Save to class
        self.name:str = name
        self.surface = window.convert_alpha() if is_alpha else window.convert()
        self.frame:coord = frame
        self.background_fill:tuple = background_fill
        self.is_alpha:bool = is_alpha
        self.scroll:bool = scroll

        # Debug surface
        logging.debug(self.__str__())

    def __str__(self):
        return '''
name: {}
surface: {}
frame: {}
background_fill:{}, is_alpha:{}'''.format(self.name, self.surface, self.frame, self.background_fill, self.is_alpha)