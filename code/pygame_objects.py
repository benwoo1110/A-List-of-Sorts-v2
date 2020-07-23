######################################
# Import and initialize the librarys #
######################################
import os
import glob
import textwrap
import inspect
import random
import math
import time
from pygame_events import *


####################
# Global variables #
####################
time_per_frame = 1 / config.ticks


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

    def size(self) -> tuple: return (self.w, self.h)

    def coord(self, surfaceCoord:tuple = (0, 0)) -> tuple: return (self.x + surfaceCoord[0], self.y + surfaceCoord[1])
    
    def rect(self): return (self.x, self.y, self.w, self.h)

    def move(self, x, y):
        og_scale = self.scale
        self.scale = False
        self.x += x
        self.y += y
        self.scale = og_scale

    def mouseIn(self, surfaceCoord:tuple = (0, 0)) -> bool:
        # Get current mouse position
        mousePos = pygame.mouse.get_pos()
        # Save surface coord to seperate variables
        scroll_x, scroll_y = surfaceCoord
        # Return if in box
        return self.x + scroll_x < mousePos[0] < self.x + self.w + scroll_x and self.y + scroll_y < mousePos[1] < self.y + self.h + scroll_y
    
    def __str__(self): return '{}'.format(self.__dict__)


class screen(coreFunc):
    def __init__(self, name: str, surfaceParameters:dict = {}, objectsParameters:dict = {}, keyboardParameters:dict = {}, actionParameters:dict = {}):
        self.name = name
        self.surface = surface(self, **surfaceParameters)
        self.objects = objects(self, objectsParameters)
        self.keyboardActions = keyboardActions(self, keyboardParameters)
        self.actions = actions(self, actionParameters)
        self.event = event(self)


class surface(coreFunc):
    def __init__(self, screen, frame:coord = coord(), bgColour:tuple = pg_ess.colour.orange, isAlpha:bool = False, scroll:bool = True):
        self.__screen__ = screen
        self.frame = frame
        self.bgColour = bgColour
        self.isAlpha = isAlpha
        self.scroll = scroll
        
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

    def load(self): self.__screen__.objects.load()

    def display(self, withLoad:bool = True, newSurface:bool = False):
        # Use a new surface
        if newSurface: self.create()
        # Update to latest state of objects
        if withLoad: self.load()
        # Output to screen
        window.blit(self.Surface, self.frame.coord())
        pg_ess.core.update()


class actions(coreFunc):
    def __init__(self, screen:screen, actionsMethods:dict = {}):
        self.__screen__ = screen
        # Add keyboard actions
        for name,action_method in actionsMethods.items():
            self.add(name, action_method)

    def add(self, name, data):
        self.__dict__[name] = data


class keyboardActions(coreFunc):
    def __init__(self, screen:screen, actions:dict):
        self.__screen__ = screen
        # Add keyboard actions
        for name,action_data in actions.items():
            self.add(name, action_data)

    def add(self, name, data):
        self.__dict__[name] = key(self.__screen__, name, **data)


class key(coreFunc):
    def __init__(self, screen, name, keys:set, onKey:str = 'down', useAscii:bool = True, runclass:runclass = None):
        self.__screen__ = screen
        self.name = name
        self.keys = keys
        self.onKey = onKey
        self.useAscii = useAscii
        self.runclass = runclass


class objects(coreFunc):
    def __init__(self, screen:screen, items:dict):
        self.__screen__ = screen
        # Add objects
        for name,item_data in items.items():
            self.add(name, item_data)

    def add(self, name, item_data):
        self.__dict__[name] = item(self.__screen__, name, **item_data)

    def getObjects(self, withItems:list = ['__all__'], excludeItems:list = []):
        items_to_load = []
        # Get all items
        if withItems == ['__all__']: items_to_load = list(self.__dict__.keys())[1:]
        # Remove the ones stated to exclude
        for excludeItem in excludeItems:
            try: items_to_load.remove(excludeItem)
            except ValueError: pass

        return items_to_load

    def load(self, withItems:list = ['__all__'], excludeItems:list = [], withState:str = None):
        # Calculate items to load
        items_to_load = self.getObjects(withItems, excludeItems)
        # Load items defined
        for name in items_to_load: self.__dict__[name].load(withState)

    def display(self, withItems:list = ['__all__'], excludeItems:list = [], withState:str = None, directToScreen:bool = False):
        # Load items directly to screen
        if directToScreen:
            # Calculate items to load
            items_to_load = self.getObjects(withItems, excludeItems)
            for name in items_to_load: self.__dict__[name].display(withState, directToScreen)

        # Load items defined to surface
        else: 
            self.load(withItems, excludeItems, withState)
            self.__screen__.surface.display(withLoad=False)


class item(coreFunc):
    types = ('object', 'background', 'button', 'text', 'textfield')

    def __init__(self, screen, name:str, type:str, frame:dict, data:any = None, dataAddSelf:bool = False, 
    state:str = '', runclass:runclass = None, loadImages:bool = True, isAlpha: bool = False):
        self.__screen__ = screen
        self.name = name
        self.type = str(type)
        self.frame = objectFrame(frame)
        self.data = data
        self.dataAddSelf = dataAddSelf
        self.state = state
        self.runclass = runclass
        self.isAlpha = isAlpha

        # Add self to data
        if dataAddSelf and data != None: data['item'] = self
        
        # load images
        if loadImages: 
            self.images = images(imagePage=[screen.name, name], isAlpha=isAlpha)
            self.load()
        # No images loaded
        else: self.images = None

    def hasRunclass(self):
        return isinstance(self.runclass, runclass)
        
    def hasState(self, state:str): 
        if type(state) == str: return hasattr(self.images, self.type+state)
        return False

    def switchState(self, toState:str, directToScreen:bool = False):
        if self.state != toState and self.hasState(toState): 
            self.display(withState=toState, directToScreen=directToScreen) 

    def load(self, withState:str = None, loadData:bool = True):
        # Set state
        if self.hasState(withState): self.state = withState
        # Load item to surface
        Surface = self.__screen__.surface.Surface
        Surface.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord()))
        # Load data
        if self.data != None and loadData: self.data.load(Surface, self.frame, self.state)

    def display(self, withState:str = None, loadData:bool = True, directToScreen:bool = False):
        # Output item to screen
        if directToScreen: 
            # Set state
            if self.hasState(withState): self.state = withState
            # Display to screen
            window.blit(self.images.__dict__[self.type+self.state], (self.frame.image.coord(self.__screen__.surface.frame.coord())))
            # Display data
            if self.data != None and loadData: self.data.display(None, self.frame, self.state, True)
            pg_ess.core.update()

        # Display to surface
        else: 
            self.load(withState)
            self.__screen__.surface.display(withLoad=False)


class images(coreFunc):
    def __init__(self, imagePage:list, fileType:str = '.png', isAlpha:bool = False):
        self.imagePage = imagePage
        self.fileType = fileType
        self.isAlpha = isAlpha

        # Load the images
        image_dir_list = self.getFilesList()

        # get the image
        for image in image_dir_list:
            # Get name
            image_name = os.path.basename(image).split('.')[0]
            # Load image
            image_surface = pygame.image.load(image).convert_alpha() if isAlpha else pygame.image.load(image).convert()
            image_surface = pygame.transform.smoothscale(image_surface, (int(image_surface.get_width()*config.scale_w()), int(image_surface.get_height()*config.scale_w())))
            # Store image
            self.__dict__[image_name] = image_surface

    def getFilesList(self) -> list:
        # Define variables
        image_dir = os.path.join('surfaces', *self.imagePage, '*'+self.fileType)
        # If in code directory and not root, go back a step
        if os.path.basename(os.getcwd()) == 'code': image_dir = '../' + image_dir
        # Get list of image from dir
        return glob.glob(image_dir)


class textFormat(coreFunc):
    def __init__(self, fontType:str = None, fontSize:int = 36, colour:tuple = pg_ess.colour.white, 
    warpText:int = None, align:str = 'left', lineSpacing:int = 1):
        self.fontType = fontType
        self.fontSize = int(fontSize * config.scale_w())
        self.colour = colour
        self.warpText = warpText
        self.align = align
        self.lineSpacing = lineSpacing
        
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

    def setText(self, text:str = None, prefix:str = None, suffix:str = None, withDisplay: bool = True):
        if text != None: self.text = text
        if prefix != None: self.prefix = prefix
        if suffix != None: self.suffix = suffix

        self.item.display()

    def renderText(self, frame:objectFrame, state:str):
        # Generate surface for text
        text_surface = pygame.surface.Surface(frame.text.size(), pygame.SRCALPHA)
        # Get text with prefix and suffix
        text = self.getText(state)
        
        # No warpText
        if self.format.warpText == None:
            text_surface.blit(self.format.font.render(text, True, self.format.colour), (0, 0))

        # Output multi-line text
        else:
            # Warp the text
            warpped_text = textwrap.wrap(text, width=self.format.warpText)
            # Print text to surface
            h = 0
            for line in warpped_text:
                # Render the text line and store to text surface
                rendered_text = self.format.font.render(line, True, self.format.colour)
                text_surface.blit(rendered_text, (0, h))
                # Set hight of next line
                h += self.format.font.size(line)[1] * self.format.lineSpacing
            
        return text_surface

    def load(self, Surface, frame:objectFrame, state:str):
        # Get the text
        text_surface = self.renderText(frame, state)
        # Output to surface
        Surface.blit(text_surface, frame.text.coord())

    def display(self, screen, frame:objectFrame, state:str, directToScreen:bool = False):
        if directToScreen:
            # Get the text
            text_surface = self.renderText(frame, state)
            # Output to screen
            window.blit(text_surface, frame.text.coord(self.item.__screen__.surface.frame.coord()))
        
        else:
            self.load(screen.surface.Surface, frame, state)
            screen.surface.display(withLoad=False)


class sortbars(coreFunc):

    def __init__(self, bars:int):
        self.bars = bars

    def __setattr__(self, name, value):
        if name == 'bars': 
            self.__dict__[name] = value
            self.calBarInfo()
        else: self.__dict__[name] = value

    def calBarInfo(self):
        # max height: 400
        # start x: 100
        # max width: 836
        # Base y: 575
        self.spacing = int(100 / self.bars)
        self.corner = int(200 / self.bars)

        self.height = int(400 / self.bars)
        self.width = int((836 - self.spacing*self.bars) / self.bars)

        self.start_x = int(100 + (836 % self.bars) / 2)
        self.base_y = 575

        # Generate random list of sort
        barsnumbers = random.sample(list(range(1, self.bars+1)), self.bars)

        # Generate barslist 
        barslist = []
        for index,bar in enumerate(barsnumbers):
            barslist.append(barData(number=bar, frame=self.calBarCoord(index, bar), colour=pg_ess.colour.white))
        
        # Store
        self.barslist = barslist

    def calBarCoord(self, index:int, bar:int) -> coord:
        return coord(
                    True, 
                    self.start_x+self.spacing//2+(self.width+self.spacing)*index, 
                    self.base_y-self.height*bar, self.width, self.height*bar
                )

    def swap(self, bar_1:int, bar_2:int, speed:float):
        # Ensure bar 2 is on the left of bar 1
        bar_1 = min(bar_1, bar_2)
        bar_2 = max(bar_1, bar_2)

        # Change colour
        self.barslist[bar_1].colour = pg_ess.colour.green
        self.barslist[bar_2].colour = pg_ess.colour.red

        # Calculate animation speed
        length_apart = self.barslist[bar_2].frame.x - self.barslist[bar_1].frame.x
        number_of_frames = config.ticks * speed
        if number_of_frames < 1: number_of_frames = 1

        move_per_frame = length_apart / number_of_frames
        
        # Animate frame
        to_move, length_moved = 0, 0
        while length_moved < length_apart:
            to_move += move_per_frame

            self.barslist[bar_1].frame.move(to_move//1, 0)
            self.barslist[bar_2].frame.move(0 - to_move//1, 0)

            length_moved += to_move//1
            to_move -= to_move//1

            self.item.load()
            self.item.__screen__.objects.time_taken.data.updateTimer()
            pg_ess.core.buffer()

        # Swap bar position
        self.barslist[bar_1], self.barslist[bar_2] = self.barslist[bar_2], self.barslist[bar_1]
        self.barslist[bar_1].frame = self.calBarCoord(bar_1, self.barslist[bar_1].number)
        self.barslist[bar_2].frame = self.calBarCoord(bar_2, self.barslist[bar_2].number)

        # Change back
        self.barslist[bar_1].colour = pg_ess.colour.white
        self.barslist[bar_2].colour = pg_ess.colour.white

        self.item.display()

    def move(self, orginal_pos:int, new_pos:int, speed:float):
        # Set colour for bar that is moving
        for i in range(min(orginal_pos, new_pos), max(orginal_pos, new_pos)+1):
             self.barslist[i].colour = pg_ess.colour.red
        self.barslist[orginal_pos].colour = pg_ess.colour.green

        # Calculate animation speed
        length_apart = self.barslist[new_pos].frame.x - self.barslist[orginal_pos].frame.x
        number_of_frames = config.ticks * speed
        if number_of_frames < 1: number_of_frames = 1

        move_per_frame = length_apart / number_of_frames
        move_other_per_frame = (self.spacing + self.width) / number_of_frames
        if length_apart > 0: move_other_per_frame = -move_other_per_frame

        # Animate moving
        to_move, length_moved = 0, 0
        while length_moved < abs(length_apart):
            # move the orginal_pos bar
            to_move += move_per_frame

            self.barslist[orginal_pos].frame.move(to_move//1, 0)

            length_moved += abs(to_move//1)
            to_move -= to_move//1

            # Move the other bars inbetween
            for i in range(min(orginal_pos, new_pos), max(orginal_pos, new_pos)+1):
                if i != orginal_pos: self.barslist[i].frame.move(move_other_per_frame, 0)

            self.item.load()
            self.item.__screen__.objects.time_taken.data.updateTimer()
            pg_ess.core.buffer()

        # Move the position of the bar in list
        value = self.barslist.pop(orginal_pos)
        self.barslist.insert(new_pos, value)

        # Re-calculate coordinates and change back colour
        for i in range(min(orginal_pos, new_pos), max(orginal_pos, new_pos)+1):
            self.barslist[i].colour = pg_ess.colour.white
            self.barslist[i].frame = self.calBarCoord(i, self.barslist[i].number)

        self.item.display()

    def completed(self):
        # Going up
        for index in range(len(self.barslist)):
            self.barslist[index].colour = (0, 255, 0)

            self.item.display()
            pg_ess.core.buffer()
            select_time = time.time()
            while time.time() - select_time < 1/self.bars: pg_ess.core.buffer()

        # Going down
        for index in range(len(self.barslist)-1, -1, -1):
            self.barslist[index].colour = pg_ess.colour.white

            self.item.display()
            pg_ess.core.buffer()
            select_time = time.time()
            while time.time() - select_time < 1/self.bars: pg_ess.core.buffer()

    def load(self, Surface, frame:objectFrame, state:str):
        for index,bar in enumerate(self.barslist):
            pygame.draw.rect(
                surface=Surface, color=bar.colour, rect=bar.frame.rect(), 
                border_top_left_radius=self.corner, border_top_right_radius=self.corner
                )

    def display(self, screen, frame:objectFrame, state:str, directToScreen:bool = False):
        self.load(screen.surface.Surface, frame, state)
        screen.surface.display(withLoad=False)


class barData(coreFunc):
    def __init__(self, number:int, frame:coord, colour:tuple = pg_ess.colour.white):
        self.number = number
        self.frame = frame
        self.colour = colour

    def state(self, withState:str = ''):
        if withState == 'selected': self.colour = pg_ess.colour.selected
        else: self.colour = pg_ess.colour.white


class timer(text):
    def __init__(self, format:textFormat = textFormat()):
        super().__init__('0.00 sec', '', '', format, False)

        self.resetTimer()

    def startTimer(self, withReset = False):
        # Start only if timer is stopped
        if self.state == 'stop':
            if withReset: self.startTime = None
            if self.startTime == None: self.startTime = time.time()
            else: self.startTime += time.time()
            self.state = 'start'
        
        else: print('Timer has alr started.')

    def stopTimer(self):
        # Stop only if timer has started
        if self.state == 'start':
            stopTime = time.time()
            self.updateTimer()
            self.startTime = stopTime - self.startTime
            self.state = 'stop'

        else: print('Timer has alr stopped.')

    def updateTimer(self):
        # Only update if timer has started
        if self.state == 'start':
            self.text = '{:.2f} sec'.format(time.time() - self.startTime)
            self.item.display()

        else: print('Cant update timer, it is currently stopped.')

    def resetTimer(self):
        self.startTime = None
        self.state = 'stop'