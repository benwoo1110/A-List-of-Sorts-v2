import  pygame

from code.api.core.Screen import Screen
from code.api.core.Window import Window
from code.api.core.Frame import Frame
from code.api.data.Images import Images


class Surface:
    def __init__(self, screen, name, frame:Frame, selectable:bool = True, 
    bg_colour:tuple = None, directDisplay:bool = False, alpha:bool = False, **items):
        self.screen = screen
        self.name = name
        self.frame = frame
        self.selectable = selectable
        self.bg_colour = bg_colour
        self.directDisplay = directDisplay
        self.alpha = alpha

        # Create surface
        if self.alpha: self.Surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        else: self.Surface = pygame.surface.Surface(self.frame.size())
        
        # Get background image
        self.bg_image = Images([self.screen.name, self.name], frame=self.frame, alpha=alpha)
        self.loadBackground()

        # Store items
        self.loaded = False
        self.containerList = []
        for name, itemData in items.items(): self.addItem(name, itemData)

    def addChild(self, name, itemData:dict):
        pass

    def getChild(self, name:str) -> Surface:
        pass

    def listChild(self) -> list:
        pass

    def unload(self):
        if self.loaded: self.loaded = False
        else: logger.warn('Surface {} already unloaded.'.format(self.name))

    def load(self, withItems:list = None, refresh:bool = False):
        # Get item list to load
        if withItems == None: toLoad = []
        elif withItems == 'all': toLoad = self.containerList
        else: toLoad = withItems
        
        # Load all items defined
        for item in toLoad: 
            if refresh: getattr(self, item).load(withData='all')
            else: getattr(self, item).load()

        # Load to screen
        self.screen.Screen.blit(self.Surface, self.frame.coord())

        self.loaded = True

    def loadBackground(self):
        # Fill colour
        if self.bg_colour != None: self.Surface.fill(self.bg_colour)
        # Display to screen
        if 'background' in self.bg_image.containerList: 
            self.Surface.blit(self.bg_image.background, (0, 0))

    def display(self, withItems:list = None, refresh:bool = False):        
        # Load the surface with items
        self.load(withItems, refresh)

        # Directly display to window
        if self.directDisplay:
            # Resize surface
            resizedSurface = pygame.transform.smoothscale(self.Surface, self.frame.size(scale=window.scale))
            
            # Output to window
            window.Window.blit(resizedSurface, self.frame.coord(surfaceCoord=window.coord(), scale=window.scale))
            PgEss.updateWindow()
        
        else:
            # Load to screen
            self.screen.display()