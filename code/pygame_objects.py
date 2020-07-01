######################################
# Import and initialize the librarys #
######################################
import os
import glob
import textwrap
from pygame_events import *


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
    
    def mouseIn(self, surfaceCoord:tuple = (0, 0)) -> bool:
        # Get current mouse position
        mousePos = pygame.mouse.get_pos()
        # Save surface coord to seperate variables
        scroll_x, scroll_y = surfaceCoord
        # Return if in box
        return self.x + scroll_x < mousePos[0] < self.x + self.w + scroll_x and self.y + scroll_y < mousePos[1] < self.y + self.h + scroll_y
    
    def __str__(self): return '{}'.format(self.__dict__)


class screen(coreFunc):
    def __init__(self, name: str, surfaceParameters:dict, objectsParameters:dict = {}):
        self.name = name
        self.surface = surface(self, **surfaceParameters)
        self.objects = objects(self, objectsParameters)
        self.event = event(self)


class surface(coreFunc):
    def __init__(self, screen, frame:coord, bgColour:tuple = pg_ess.colour.orange, isAlpha:bool = False):
        self.__screen__ = screen
        self.frame = frame
        self.bgColour = bgColour
        self.isAlpha = isAlpha
        
        # Create surface
        self.create()
    
    def create(self):
        # Create window based on if is alpha
        if self.isAlpha: Surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        else: Surface = pygame.surface.Surface(self.frame.size())
        # set background color
        if self.bgColour != None: Surface.fill(self.bgColour)
        # Save Surface to class
        self.Surface = Surface
    
    def fill(bgColour:tuple = None):
        pass

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

    def display(self, items:tuple = None, withState:str = None, directToScreen:bool = False):
        if directToScreen:
            # Display all items
            if items == None:
                for name,item in self.__dict__.items():
                    if name != '__screen__': item.display(withState, directToScreen)
            # Load items defined
            else:
                for name in items:
                    self.__dict__[name].display(state, directToScreen)

        else: 
            # Load items defined to surface
            self.load(items, state)
            # Display Surface
            self.__screen__.surface.display(withLoad=False)


class item(coreFunc):
    types = ('object', 'background', 'button', 'text', 'textfield')

    def __init__(self, screen, name:str, type:str, frame:dict, data:any = None,dataAddSelf:bool = False, state:str = '',
    runclass:any = None, runclassParameter:any = {}, loadImages:bool = True, isAlpha: bool = False):
        self.__screen__ = screen
        self.name = name
        self.type = str(type)
        self.frame = objectFrame(frame)
        self.data = data
        self.dataAddSelf = dataAddSelf
        self.state = state
        self.runclass = runclass
        self.runclassParameter = runclassParameter
        self.loadImages = loadImages
        self.isAlpha = isAlpha

        # Add self to data
        if dataAddSelf: data['item'] = self
        
        # load images
        if loadImages: 
            self.images = images(imagePage=(screen.name, name), isAlpha=isAlpha)
            self.load()
        # No images loaded
        else: self.images = None
        
    def hasState(self, state:str): 
        if type(state) == str: return hasattr(self.images, self.type+state)
        return False

    def switchState(self, toState:str, directToScreen:bool = False):
        if self.state != toState and self.hasState(toState): 
            self.display(toState, directToScreen) 

    def load(self, withState:str = None, loadData:bool = True):
        # Set state
        if self.hasState(withState): self.state = withState
        # Load item to surface
        Surface = self.__screen__.surface.Surface
        Surface.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord()))
        # Load data
        if self.data != None and loadData: self.data.load(Surface, self.frame, self.state)

    def display(self, withState:str = None, directToScreen:bool = False):
        # Output item to screen
        if directToScreen: 
            # Set state
            if self.hasState(withState): self.state = withState
            # Display to screen
            window.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord()))
            pg_ess.core.update()
        # Display to surface
        else: 
            self.load(withState)
            self.__screen__.surface.display(withLoad=False)


class images(coreFunc):
    def __init__(self, imagePage:tuple, fileType:str = '.png', isAlpha:bool = False):
        self.imagePage = imagePage
        self.fileType = fileType
        self.isAlpha = isAlpha

        # Load the images
        image_dir_list = self.getFilesList()

        # get the image
        for image in image_dir_list:
            # Load image
            image_name = image.split('/')[-1].split('\\')[-1].split('.')[0]
            image_surface = pygame.image.load(image).convert_alpha() if isAlpha else pygame.image.load(image).convert()
            image_surface = pygame.transform.smoothscale(image_surface, (int(image_surface.get_width()*config.scale_w()), int(image_surface.get_height()*config.scale_w())))
            # Store image
            self.__dict__[image_name] = image_surface

    def getFilesList(self) -> list:
        # Define variables
        image_dir = 'surfaces/{}/'.format('/'.join(self.imagePage))
        # If in code directory and not root, go back a step
        if os.path.basename(os.getcwd()) == 'code': image_dir = '../' + image_dir
        # Get all image file from givent directory
        return glob.glob(image_dir+"*"+self.fileType)


class textFormat(coreFunc):
    def __init__(self, fontType:str = None, fontSize:int = 36, 
    colour:tuple = pg_ess.colour.white, warpText:int = None, align:str = 'left'):
        self.fontType = fontType
        self.fontSize = int(fontSize * config.scale_w())
        self.colour = colour
        self.warpText = warpText
        self.align = align
        
        self.font = pygame.font.Font(self.fontType, self.fontSize)


class text(coreFunc):
    def __init__(self, text:str = '', prefix:str = '', suffix:str = '', 
    format:textFormat = textFormat(), editable:bool = True):
        self.text = text
        self.prefix = prefix
        self.suffix = suffix
        self.format = format
        self.editable = editable

    def getText(self, state:str):
        if state == 'Selected' and self.editable: return self.prefix+self.text+'_'+self.suffix
        else: return self.prefix+self.text+self.suffix

    def load(self, Surface, frame:objectFrame, state:str):
        text = self.getText(state)
        # No warpText
        if self.format.warpText == None:
            rendered_text = self.format.font.render(text, True, self.format.colour)
            Surface.blit(rendered_text, frame.text.coord())

        # Output multi-line text
        else:
            # Warp the text
            warpped_text = textwrap.wrap(text, width=self.format.warpText)
            # Generate surface for text
            text_surface = pygame.surface.Surface(frame.text.size())
            # Print text to surface
            h = 0
            for line in warpped_text:
                rendered_text = self.format.font.render(line, True, self.format.colour)
                text_surface.blit(rendered_text, (0, h))
                h += self.format.font.size(line)[1]
            # Output to surface
            Surface.blit(text_surface, frame.text.coord())