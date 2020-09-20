import pygame

from code.api.core.Container import Container
from code.api.utils.File import File
from code.api.utils.Logger import Logger


class Window(Container):
    def __init__(self, icon:File, title:str, fullscreen:bool, windowScale:int, size:tuple):
        super().__init__()
        self.screensStack = []
        self.doStackChange = False
        self.doUpdate = False

        # Set icon
        try: pygame.display.set_icon(pygame.image.load(icon.getPath()))
        except FileNotFoundError: Logger.get().error('No app icon image found at {}'.format(icon.getPath()))
        except Exception: Logger.get().error('Error loading app icon image {}!'.format(icon.getPath()), exc_info=True)

        # Set title
        try: pygame.display.set_caption(title)
        except Exception: Logger.get().error('Unable set display caption!', exc_info=True)

        # Set display
        self.width = size[0]
        self.height = size[1]

        if fullscreen:
            self.window = pygame.display.set_mode(self.size(), pygame.FULLSCREEN)

            # Get fullscreen window size
            windowWidth, windowHeight = self.window.get_size()
            
            # Set scaling
            self.scale = min(windowWidth / width, windowHeight / height)
            self.scaledWidth = int(self.width * self.scale)
            self.scaledWeight = int(self.height * self.scale)

            # Set coord to be center
            self.x = int((windowWidth - self.scaledWidth) / 2)
            self.y = int((windowHeight - self.scaledWeight) / 2)

        else: 
            # Set scaling
            self.scale = windowScale
            self.scaledWidth = int(self.width * self.scale)
            self.scaledWeight = int(self.height * self.scale)

            # Set coord
            self.x = 0
            self.y = 0

            self.window = pygame.display.set_mode(self.scaledSize())

        # Show display information
        Logger.get().debug(pygame.display.Info())

    def update(self):
        try:
            resizedSurface = pygame.transform.smoothscale(self.getCurrentScreen(), self.scaledSize())
            self.window.blit(resizedSurface, self.getCoord())
            pygame.display.update()
            pygame.time.Clock().tick(60)

        except Exception as e:
            Logger.get().critical(e, exc_info=True)
            Logger.get().critical('Error updating pygame window!')

        self.doUpdate = False

    def changeStack(self, type_:str, screen:str = None) -> bool:
        # Notify another changeStack() is happening
        if self.stackChange: 
            Logger.get().warning('Another stack change is happening as well, this may cause issues.')
        
        self.doStackChange = True

        # Go back to previous screen
        if str(type_) == 'back':
            # Go back one screen
            if screen == None: self.screensStack.pop()
            # Go back to screen specified
            elif screen in self.screens:
                self.screensStack = self.screensStack[:self.screensStack.index(screen)+1]
            # Error
            else:
                Logger.get().error('"{}" is not a screen.'.format(screen))
                return False
        
        # Load a new screen
        elif type_ == 'load':  
            if screen in self.screens:
                self.screensStack.append(screen)
            # Error
            else:
                Logger.get().error('"{}" is not a screen.'.format(screen))
                return False

        # Error
        else: 
            Logger.get().error('{} type not recognised.'.format(type_))
            return False
        
        # Log change
        Logger.get().debug('Change stack completed with type:{} screen:{}'.format(type_, screen))
            
        return True

    def mainloop(self, startScreen:str):
        # Start with startScreen
        self.screensStack.append(startScreen)

        while True:
            # fallback to startScreen
            if len(self.screensStack) == 0: 
                self.screensStack.append(startScreen)
                Logger.get().error('No screen in stack, falling back to startScreen.')

            # Prep screen
            screen = self.container.get(self.screensStack[-1])
            screen.start()
            screen.display()

            # Log current screen stacks
            Logger.get().debug('New screen stack of {}'.format(self.screensStack))
            
            # Main loop for top screen
            while not self.doStackChange:
                # Check for updates wanted to screen
                if self.doUpdate: self.update()

                # Get result of screen actions
                screenResult = screen.run()

                # End program
                if screenResult == 'quit':
                    pygame.quit()
                    return

            # When screen ends
            screen.end()
            self.doStackChange = False

    def addScreen(self, screen):
        self.container[screen.getName()] = screen
        Logger.get().debug('Added screen {}'.format(screen.getName()))

    def triggerUpdate(self):
        self.doUpdate = True

    def size(self): return (self.width, self.height)

    def scaledSize(self): return (self.scaledWidth, self.scaledWeight)

    def getCoord(self): return (self.x, self.y)

    def getCurrentScreen(self): return self.container.get(self.screensStack[-1]).getScreen()
