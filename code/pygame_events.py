######################################
# Import and initialize the librarys #
######################################
from pygame_core import *


class eventRun(coreFunc):
    def __init__(self, action:str, event:any, parameters:list = []): 
        self.action = action
        self.event = event
        self.parameters = parameters


class eventResults(coreFunc):
    def __init__(self, **kwargs): 
        self.__dict__.update(kwargs)

    def didAction(self, action = None): 
        # Check if there was an action
        if action == None: return self.__dict__ != {}
        # Check for specific action
        else: return hasattr(self, action)


class actionResult(coreFunc):
    def __init__(self, name:str, type:str, outcome:any = None): 
        self.name = name
        self.type = str(type)
        self.outcome = outcome


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

    def action(self, direct_to_screen:bool = False):
        for name,item in self.__screen__.objects.__dict__.items():
            # Check if item is valid and has a runclass
            if name !=  '__screen__' and item.runclass != None: 
                while item.frame.box.mouseIn(pygame.mouse.get_pos(),  self.__screen__.surface.frame.coord()):
                    # Load hover state
                    item.switchState('Hover', direct_to_screen) 
                    
                    # Check for clicks
                    event_result = self.Event([
                        eventRun(action='click', event=self.click, parameters=[item, direct_to_screen]),
                        eventRun(action='scroll', event=self.scroll),
                        eventRun(action='quit', event=self.quit)
                        ])
                    if event_result.didAction(): return event_result

                # Change back to normal state
                item.switchState('', direct_to_screen) 

        # Run event
        event_result = self.Event([
                eventRun(action='scroll', event=self.scroll),
                eventRun(action='quit', event=self.quit)
                ])
        if event_result.didAction(): return event_result

    def click(self, event, item, direct_to_screen:bool = False):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #
            click_result = actionResult(name=item.name, type=item.type)
            item.switchState('Selected')

            # Runclass is just a string
            if type(item.runclass) == str: click_result.outcome = item.runclass
            # Runclass is a method
            else: click_result.outcome = item.runclass(**item.runclass_parameter)

            return click_result

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
            return 'quit'