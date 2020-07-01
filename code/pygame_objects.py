######################################
# Import and initialize the librarys #
######################################
import os
import glob
from pygame_events import *

##################
# Initialization #
##################
window = pygame.display.set_mode(config.screen_res())


class coreFunc:
    def __setitem__(self, name, value): self.__dict__[name] = value
    def __setattr__(self, name, value): self.__dict__[name] = value
    def __getitem__(self, name): return self.__dict__[name]
    def __str__(self): return '{}'.format(self.__dict__)


class objectFrame(coreFunc):
    def __init__(self, coords):
        self.__dict__.update(**coords)

class coord:
    def __init__(self, scale:bool = True, x:int = 0, y:int = 0, w:int = 0, h:int = 0):
        self.scale:bool = scale
        self.x:int = x
        self.y:int = y
        self.w:int = w
        self.h:int = h

    def __setattr__(self, name, value):
        if name != 'scale' and self.scale: self.__dict__[name] = int(value * config.scale_w())
        else: self.__dict__[name] = value

    def size(self) -> tuple: 
        return (self.w, self.h)

    def coord(self, surfaceCoord:tuple = (0, 0)) -> tuple: 
        return (self.x + surfaceCoord[0], self.y + surfaceCoord[1])
    
    def mouseIn(self, mouse_pos:tuple, surfaceCoord:tuple = (0, 0)) -> bool:
        # Save surface coord to seperate variables
        scroll_x, scroll_y = surfaceCoord
        # Return if in box
        return self.x + scroll_x < mouse_pos[0] < self.x + self.w + scroll_x and self.y + scroll_y < mouse_pos[1] < self.y + self.h + scroll_y
    
    def __str__(self): return '{}'.format(self.__dict__)


class screen(coreFunc):
    def __init__(self, name: str, surface_parameters:dict, objects_parameters:dict = {}):
        self.name = name
        self.surface = surface(self, **surface_parameters)
        self.objects = objects(self, objects_parameters)
        self.event = event(self)


class surface(coreFunc):
    def __init__(self, screen, frame:coord, bg_colour:tuple = pg_ess.colour.orange, is_alpha:bool = False):
        self.__screen__ = screen
        self.frame = frame
        self.bg_colour = bg_colour
        self.is_alpha = is_alpha
        
        # Create surface
        self.create()
    
    def create(self):
        # Create window based on if is alpha
        if self.is_alpha: Surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        else: Surface = pygame.surface.Surface(self.frame.size())
        # set background color
        if self.bg_colour != None: Surface.fill(self.bg_colour)
        # Save Surface to class
        self.Surface = Surface

    def load(self): self.__screen__.objects.load()

    def display(self, withLoad:bool = True):
        # Update to latest state of objects
        if withLoad: self.load()
        # Output to screen
        window.blit(self.Surface, self.frame.coord())
        pg_ess.core.update()


class objects(coreFunc):
    def __init__(self, screen, items):
        self.__screen__ = screen
        # Add objects
        for name,item_data in items.items():
            self.add(name, item_data)

    def add(self, name, item_data):
        self.__dict__[name] = item(self.__screen__, name, **item_data)

    def load(self, items:tuple = None, withState:str = None):
        # Load all items
        if items == None:
            for name,item in self.__dict__.items():
                if name != '__screen__': item.load(withState)
        # Load items defined
        else:
            for name in items:
                self.__dict__[name].load(withState)

    def display(self, items:tuple = None, withState:str = None, direct_to_screen:bool = False):
        if direct_to_screen:
            # Display all items
            if items == None:
                for name,item in self.__dict__.items():
                    if name != '__screen__': item.display(state, direct_to_screen)
            # Load items defined
            else:
                for name in items:
                    self.__dict__[name].display(state, direct_to_screen)

        else: 
            # Load items defined to surface
            self.load(items, state)
            # Display Surface
            self.__screen__.surface.display(withLoad=False)


class item(coreFunc):
    types = ('object', 'background', 'button', 'text', 'textfield')

    def __init__(self, screen, name:str, type:str, frame:dict, data:any = None, state:str = '',
    runclass:any = None, runclass_parameter:any = {}, load_images:bool = True):
        self.__screen__ = screen
        self.name = name
        self.type = str(type)
        self.frame = objectFrame(frame)
        self.data = data
        self.state = state
        self.runclass = runclass
        self.runclass_parameter = runclass_parameter
        
        # load images
        if load_images: 
            self.images = images((screen.name, name))
            self.load()
        # No images loaded
        else: self.images = None
        
    def hasState(self, state:str): 
        return hasattr(self.images, self.type+state)

    def switchState(self, toState:str, direct_to_screen:bool = False):
        if self.state != toState and self.hasState(toState): 
            self.display(toState, direct_to_screen) 

    def load(self, withState:str = None):
        # Set state
        if withState != None: self.state = withState
        # Load item to surface
        Surface = self.__screen__.surface.Surface
        Surface.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord()))
        # Load data
        if self.data != None: self.data.load()

    def display(self, withState:str = None, direct_to_screen:bool = False):
        # Output item to screen
        if direct_to_screen: 
            # Set state
            if withState != None: self.state = withState
            # Display to screen
            window.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord()))
            pg_ess.core.update()
        # Display to surface
        else: 
            self.load(withState)
            self.__screen__.surface.display(withLoad=False)


class images:
    def __init__(self, imagePage:tuple, fileType:str = '.png', isAlpha:bool = False):
        self.imagePage = imagePage
        self.fileType = fileType
        self.isAlpha = isAlpha

        # Load the images
        image_dir_list = self.get_files()

        # get the image
        for image in image_dir_list:
            # Load image
            image_name = image.split('/')[-1].split('\\')[-1].split('.')[0]
            image_surface = pygame.image.load(image).convert_alpha() if isAlpha else pygame.image.load(image).convert()
            image_surface = pygame.transform.smoothscale(image_surface, (int(image_surface.get_width()*config.scale_w()), int(image_surface.get_height()*config.scale_w())))
            # Store image
            self.__dict__[image_name] = image_surface

    def get_files(self) -> list:
        # Define variables
        image_dir = 'surfaces/{}/'.format('/'.join(self.imagePage))
        # If in code directory and not root, go back a step
        if os.path.basename(os.getcwd()) == 'code': image_dir = '../' + image_dir
        # Get all image file from givent directory
        return glob.glob(image_dir+"*"+self.fileType)


class text(coreFunc):
    def __init__(self, text:str = '', font_type:str = None, calculate_font_dir:bool = True, 
    font_size:int = 36, warp_text:int = None, align:str = 'left', colour:set = (0, 0, 0), validation = None):
        pass

    def load(self):
        pass