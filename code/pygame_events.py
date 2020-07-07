######################################
# Import and initialize the librarys #
######################################
from pygame_core import *


# Track keys that are pressed
keypressed = set()


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
        # Runclass is just a string
        if not callable(item.runclass.action): self.outcome = item.runclass.action
        # Runclass is a method
        elif item.runclass.includeScreen: self.outcome = item.runclass.action(item.__screen__, **item.runclass.parameters)
        # Do not add 
        else: self.outcome = item.runclass.action(**item.runclass.parameters)

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
                event_result = event_run.event(event, *event_run.parameters)
                if event_result != None:
                    result[event_run.action] = event_result
        
        return result

    def action(self, directToScreen:bool = False):
        for index,name in enumerate(list(self.__screen__.objects.__dict__.keys())[1:]):
            # Get item
            item = self.__screen__.objects[name]
            # Check if has a runclass and mouse in hovering over it
            while item.hasRunclass() and item.frame.box.mouseIn(self.__screen__.surface.frame.coord()):
                # Load hover state
                item.switchState('Hover', directToScreen) 
                
                # Check for clicks
                event_result = self.Event([
                    eventRun(action='click', event=self.click, parameters=[item, directToScreen]),
                    eventRun(action='keyboard', event=self.keyboard),
                    eventRun(action='scroll', event=self.scroll),
                    eventRun(action='quit', event=self.quit)
                    ])
                if event_result.didAction(): return event_result

                # Check if mouse pos on more important layers
                priority = False
                for priority_name in list(self.__screen__.objects.__dict__.keys())[index+2:]:
                    priority_item = self.__screen__.objects[priority_name]
                    if priority_item.hasRunclass() and priority_item.frame.box.mouseIn(self.__screen__.surface.frame.coord()):
                        priority = True
                        break
                if priority: break

            # Change back to normal state
            item.switchState('', directToScreen) 

        # Run event
        event_result = self.Event([
                eventRun(action='keyboard', event=self.keyboard),
                eventRun(action='scroll', event=self.scroll),
                eventRun(action='quit', event=self.quit)
                ])
        if event_result.didAction(): return event_result

    def click(self, event, item, directToScreen:bool = False):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Set state to clicked
            click_result = actionResult(name=item.name, type=item.type, outcome='clicked')
            item.switchState('Selected')
            
            # Get the outcome of running
            click_result.getOutcome(item)

            # Output result
            return click_result

    def keyboard(self, event):
        keyboard_result = None

        # When key is pressed
        if event.type == pygame.KEYDOWN:
            keypressed.add(event.key)
            keyboard_result = actionResult(name=event.key, type='keydown', outcome='pressed')

        # When key is released
        elif event.type == pygame.KEYUP:
            keypressed.discard(event.key)
            keyboard_result = actionResult(name=event.key, type='keyup', outcome='released')

        # When there was an action
        if keyboard_result != None:
            # Check if key that was pressed have action to run
            for name in list(self.__screen__.keyboardActions.__dict__.keys())[1:]:
                key = self.__screen__.keyboardActions[name]

                # On match key state and match key
                if ( (key.onKey == 'down' and keyboard_result.isType('keydown')) or (key.onKey == 'up' and keyboard_result.isType('keyup')) ) and keypressed.intersection(key.keys) != set():
                    # Set name of result
                    keyboard_result.name = key.name
                    # Get the outcome of running
                    keyboard_result.getOutcome(key)     
            
        return keyboard_result

    def scroll(self, event):
        # Get surface
        surface = self.__screen__.surface
        # Check if scrolling is needed
        if config.screen.height - surface.frame.h < 0:
            # Check of scroll action
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Scroll up
                if event.button == 4:
                    surface.frame.y = min(surface.frame.y + config.scroll_speed, 0) / config.scale_w()
                    surface.display(withLoad=False)
                # Scroll down
                elif event.button == 5:
                    surface.frame.y = max(surface.frame.y - config.scroll_speed, min(config.screen.height - surface.frame.h, 0)) / config.scale_w()
                    surface.display(withLoad=False)

    def quit(self, event):
        if event.type == pygame.QUIT: 
            return '__quit__'