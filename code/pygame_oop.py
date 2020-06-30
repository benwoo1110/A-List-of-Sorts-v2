######################################
# Import and initialize the librarys #
######################################
import logging
import os
import glob
import pygame
from config import config


##################
# Initialization #
##################
pygame.init()
window = pygame.display.set_mode(config.screen_res())


######################
# Essentials Classes #
######################
class pg_ess:

    ##########################
    # Common defined colours #
    ##########################
    class colour:
        '''Common colour types in RGB tuple form'''
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        gray = (43, 43, 43)
        whiteish = (213, 213, 213)
        orange = (255, 143, 8)
    

    ##################
    # Core functions #
    ##################
    class core:
        def set_caption(caption:str = 'pygame time!'):
            '''Set window header title'''
            pygame.display.set_caption(caption)
            logging.debug('window captions set to {}'.format(caption))

        def update(tick:int = config.ticks):
            '''Draw display changes to screen'''
            pygame.display.flip()
            pygame.display.update()
            pygame.time.Clock().tick(tick)

        def buffer() -> bool:
            '''Loop through pygame events and check of quit and scrolling'''
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return True
                # pygame_ess.event.scroll(window, event)

        def quit():
            '''Exit from program'''
            logging.info('Exiting program...')
            pygame.quit()


class coord:
    def __init__(self, bx:int = 0, by:int = 0, w:int = 0, h:int = 0, ix:int = 0, iy:int = 0, scale:bool = True):
        self.scale:bool = scale
        self.bx:int = bx
        self.by:int = by
        self.w:int = w
        self.h:int = h
        self.ix:int = ix
        self.iy:int = iy

    def __setattr__(self, name, value):
        if name != 'scale' and self.scale: self.__dict__[name] = int(value * config.scale_w())
        else: self.__dict__[name] = value

    def box_size(self) -> tuple: return (self.w, self.h)

    def box_coord(self, surface_coord:tuple = (0, 0)) -> tuple: return (self.bx + surface_coord[0], self.by + surface_coord[1])
    
    def image_coord(self, surface_coord:tuple = (0, 0)) -> tuple: return (self.ix + surface_coord[0], self.iy + surface_coord[1])

    def in_box(self, mouse_pos:tuple, surface_coord:tuple = (0, 0)) -> bool:
        # Save surface coord to seperate variables
        scroll_x:int = surface_coord[0]
        scroll_y:int = surface_coord[1]
        # Return if in box
        return self.frame.bx + scroll_x < mouse_pos[0] < self.frame.bx + self.frame.w + scroll_x and self.frame.by + scroll_y < mouse_pos[1] < self.frame.by + self.frame.h + scroll_y
    
    def __str__(self): return '{}'.format(self.__dict__)


class screen:
    def __init__(self, name: str, surface_parameters:dict, objects_parameters:dict = {}):
        self.name = name
        self.surface = surface(self, **surface_parameters)
        self.objects = objects(self, objects_parameters)

    def __setitem__(self, name, value): self.__dict__[name] = value

    def __setattr__(self, name, value): self.__dict__[name] = value

    def __getitem__(self, name): return self.__dict__[name]

    def __str__(self): return '{}'.format(self.__dict__)


class surface:
    def __init__(self, screen, frame:coord, bg_colour:tuple = pg_ess.colour.orange, is_alpha:bool = False):
        self.screen = screen
        self.frame = frame
        self.bg_colour = bg_colour
        self.is_alpha = is_alpha
        
        # Create surface
        self.create()
    
    def create(self):
        # Create window based on if is alpha
        if self.is_alpha: Surface = pygame.surface.Surface(self.frame.box_size(), pygame.SRCALPHA)
        else: Surface = pygame.surface.Surface(self.frame.box_size())
        # set background color
        if self.bg_colour != None: Surface.fill(self.bg_colour)
        # Save Surface to class
        self.Surface = Surface

    def load(self): self.screen.objects.load()

    def display(self, with_load:bool = True):
        # Update to latest state of objects
        if with_load: self.load()
        # Output to screen
        window.blit(self.Surface, self.frame.box_coord())
        pg_ess.core.update()

    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)


class objects:
    def __init__(self, screen, items):
        self.screen = screen
        # Add objects
        for name,item_data in items.items():
            self.add(name, item_data)

    def add(self, name, item_data):
        self.__dict__[name] = item(self.screen, name, **item_data)

    def load(self, items:tuple = None):
        # Load all items
        if items == None:
            for name,item in self.__dict__.items():
                if name != 'screen': item.load()
        # Load items defined
        else:
            for name in items:
                self.__dict__[name].load()

    def display(self, items:tuple = None, direct_to_screen:bool = False):
        if direct_to_screen:
            # Display all items
            if items == None:
                for name,item in self.__dict__.items():
                    if name != 'screen': item.display(direct_to_screen)
            # Load items defined
            else:
                for name in items:
                    self.__dict__[name].display(direct_to_screen)

        else: 
            # Load items defined to surface
            self.load(items)
            # Display Surface
            self.screen.load(with_load=False)

    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)



class item:
    types = ('object', 'background', 'button', 'text', 'textfield')

    def __init__(self, screen, name:str, type:str, frame:coord, data:any = None, 
    runclass:any = None, runclass_parameter:any = None, load_images:bool = True):
        self.screen = screen
        self.name = name
        self.type = type
        self.data = data
        self.frame = frame
        self.runclass = runclass
        self.runclass_parameter = runclass_parameter

        if load_images: self.images = images(frame, (screen.name, name))
        else: self.images = None

    def load(self, state:str = ''):
        Surface = self.screen.surface.Surface
        Surface.blit(self.images.__dict__[self.type+state], (self.frame.image_coord()))

    def display(self, state:str = '', direct_to_screen:bool = False):
        # Load the item
        self.load(state)
        # Output item to screen
        if direct_to_screen: 
            window.blit(self.images.__dict__['{}_{}'.format(self.type, '_'.join(state))], self.frame.image_coord())
            pg_ess.core.update()
        else: self.screen.surface.display(with_load=False)

    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)


class images:
    def __init__(self, frame:coord, image_page:tuple, file_type:str = '.png', is_alpha:bool = False):
        self.image_page = image_page
        self.file_type = file_type
        self.is_alpha = is_alpha

        # Load the images
        image_dir_list = self.get_files()

        # get the image
        for image in image_dir_list:
            # Load image
            image_name = image.split('/')[-1].split('\\')[-1].split('.')[0]
            image_surface = pygame.image.load(image).convert_alpha() if is_alpha else pygame.image.load(image).convert()
            image_surface = pygame.transform.smoothscale(image_surface, (int(image_surface.get_width()*config.scale_w()), int(image_surface.get_height()*config.scale_w())))
            # Store image
            self.__dict__[image_name] = image_surface

    def get_files(self) -> list:
        # Define variables
        image_dir = 'surfaces/{}/'.format('/'.join(self.image_page))
        # If in code directory and not root, go back a step
        if os.path.basename(os.getcwd()) == 'code': image_dir = '../' + image_dir
        # Get all image file from givent directory
        return glob.glob(image_dir+"*"+self.file_type)

    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)


test = screen(
    name = 'home',
    surface_parameters = {
        'frame': coord(w=1024, h=768)
    },

    objects_parameters = {
        'background': {
            'type': 'object',
            'frame': coord(w=1024, h=768)
        },
        'run': {
            'type': 'button',
            'frame': coord(
                bx=775, by=671,
                w=1024, h=768,
                ix=775, iy=671
                )
        }
    }
)


test.surface.display()
test.objects.run.display(state='_hover')

while True:
    if pg_ess.core.buffer(): break

pg_ess.core.quit()