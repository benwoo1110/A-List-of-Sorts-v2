######################################
# Import and initialize the librarys #
######################################
from code.pygame_core import *


#################
# Setup logging #
#################
filename = os.path.basename(__file__).split('.')[0]
logger = log.get_logger(filename)
logger.info('Loading up {}...'.format(filename))


# Track keys that are pressed
keypressed = []


class runclass(coreFunc):
    def __init__(self, action:any, parameters:dict = {}, includeScreen: bool = True):
        self.action = action
        self.parameters = parameters
        self.includeScreen = includeScreen


class eventRun(coreFunc):
    def __init__(self, action:str, event:any, parameters:list = []): 
        self.action = action
        self.event = event
        self.parameters = parameters


class eventResults(coreFunc):
    def __init__(self, **kwargs): 
        self.__dict__.update(kwargs)

    def didAction(self, action = None) -> bool: 
        # Check if there was an action
        if action == None: return self.__dict__ != {}
        # Check for specific action
        else: return hasattr(self, action)

    def contains(self, key:str, value:any) -> bool: 
        return any(result[key] == value for result in self.__dict__.values())


class actionResult(coreFunc):
    def __init__(self, name:str, type:str, outcome:any = None): 
        self.name = name
        self.type = str(type)
        self.outcome = outcome

    def getOutcome(self, item):
        try:
            # Runclass is just a string
            if not callable(item.runclass.action): self.outcome = item.runclass.action
            # Runclass is a method
            elif item.runclass.includeScreen: self.outcome = item.runclass.action(item.__screen__, **item.runclass.parameters)
            # Do not add screen
            else: self.outcome = item.runclass.action(**item.runclass.parameters)
        
        # There is a error
        except Exception as e: logger.error(e, exc_info=True)

    def isItem(self, name = None) -> bool: return self.name == name

    def isType(self, type = None) -> bool: return self.type == type

    def withOutcome(self, outcome = None) -> bool: return self.outcome == outcome


class event(coreFunc):

    def __init__(self, screen):
        self.__screen__ = screen

    def Event(self, events:list):
        # init event result
        result = eventResults()
        # check events
        for event in pygame.event.get():
            for event_run in events: 
                # Run events
                event_result = event_run.event(event, *event_run.parameters)
                # Get and store result if any
                if event_result != None: result[event_run.action] = event_result

        pygame.display.update()
        clock.tick(config.framerate)
        
        return result

    def action(self, actions:list = [],  directToScreen:bool = False):
        onItem = None
        # Loop through items in opposite order
        for index,name in enumerate(list(self.__screen__.objects.__dict__.keys())[1:]):
            # Get item
            item = self.__screen__.objects[name]
            # Check if has a runclass
            if item.hasRunclass():
                # Check of mouse in hovering over it
                if item.frame.box.mouseIn(self.__screen__.surface.frame.coord()):
                    # Load hover state
                    item.switchState('Hover', directToScreen) 
                    onItem = item
                # Change back to normal state
                elif item.state in ('Hover', 'Selected'): item.switchState('', directToScreen)

        # Run actions
        for actionMethod in actions:
            if hasattr(self.__screen__.actions, actionMethod): self.__screen__.actions[actionMethod]()

        # Run events
        event_result = self.Event([
            eventRun(action='click', event=self.click, parameters=[onItem, directToScreen]),
            eventRun(action='keydown', event=self.keydown),
            eventRun(action='keyup', event=self.keyup),
            eventRun(action='scroll', event=self.scroll),
            eventRun(action='resize', event=self.resize),
            eventRun(action='quit', event=self.quit)
        ])
        
        # Output event's result if any
        if event_result.didAction(): 
            logger.debug('[{}] {}'.format(self.__screen__.name, event_result))
            return event_result

    def click(self, event, item, directToScreen:bool = False):
        # Check if item is valid
        if item == None: return

        # Check if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Set state to clicked
            click_result = actionResult(name=item.name, type=item.type, outcome='clicked')
            
            # Get the outcome of running
            click_result.getOutcome(item)

            # Output result
            return click_result

    def keydown(self, event):
        keyboard_result = None
        # When key is pressed
        if event.type == pygame.KEYDOWN:
            keyboard_result = actionResult(name=event.key, type='down', outcome='pressed')
            keypressed.append(event)

        return self.keyEvent(event, keyboard_result)
        
    def keyup(self, event):
        keyboard_result = None
        # When key is released
        if event.type == pygame.KEYUP:
            keyboard_result = actionResult(name=event.key, type='up', outcome='released')
            for index, pressed in enumerate(keypressed):
                if pressed.key == event.key: keypressed.pop(index)
        
        return self.keyEvent(event, keyboard_result)

    def keyEvent(self, event, keyboard_result):
        # When there was an action
        if keyboard_result != None:
            # Check if key that was pressed have action to run
            for name in list(self.__screen__.keyboardActions.__dict__.keys())[1:]:
                key = self.__screen__.keyboardActions[name]

                # On match key state and match key
                if key.onKey == keyboard_result.type and event.key in key.keys:
                    # Set name of result
                    keyboard_result.name = key.name
                    # Get the outcome of running
                    keyboard_result.getOutcome(key) 
            
        return keyboard_result

    def scroll(self, event):
        # Get surface
        surface = self.__screen__.surface
        # Check if scrolling is needed
        if surface.scroll and config.screen.height - surface.frame.__getattr__('h', True) < 0:
            # Check of scroll action
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Scroll up
                if event.button == 4:
                    surface.frame.y = min(surface.frame.y + config.scroll_speed, 0) 
                    surface.display()
                # Scroll down
                elif event.button == 5:
                    surface.frame.y = max(surface.frame.y - config.scroll_speed, min(config.screen.height - surface.frame.__getattr__('h', scale=True), 0))
                    surface.display()

    def resize(self, event):
        if event.type == pygame.VIDEORESIZE:
            # Save new screen size
            config.screen.width = event.w
            config.screen.height = event.h

            # Set y axis to new window size
            self.__screen__.surface.frame.y = max(self.__screen__.surface.frame.y, min(config.screen.height - self.__screen__.surface.frame.__getattr__('h', scale=True), 0))
            
            # Display surface with new scaling 
            window.fill(pg_ess.colour.orange)
            resizedSurface = pygame.transform.smoothscale(pygame.display.get_surface(), event.size)
            window.blit(resizedSurface, self.__screen__.surface.frame.coord())
            
            logger.debug('Window resized to {}'.format(event.size))
        
        elif event.type == pygame.VIDEOEXPOSE:  
            window.fill(pg_ess.colour.orange)
            window.blit(pygame.display.get_surface(), self.__screen__.surface.frame.coord())
            self.__screen__.surface.display() 

            logger.debug('Window exposed...')

    def quit(self, event):
        if event.type == pygame.QUIT: 
            return actionResult(name='quit', type='quit', outcome='__quit__')