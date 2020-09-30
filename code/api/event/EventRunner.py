import pygame
from functools import wraps

from code.api.event.EventHandler import EventHandler


class EventRunner:
    def __init__(self, screen):
        self._screen = screen
        self._currentHoverSurface = None
        self._events = {
            'clickdown': self.clickdown,
            'clickup': self.clickup,
            'keydown': self.keydown,
            'keyup': self.keyup,
            'quit': self.quit
        }

    def run(self):
        self.hover()
        for PGEvent in pygame.event.get():
            for _, handler in self._events.items():
                handler(PGEvent)
    
    def hover(self):
        self._currentHoverSurface = self.getHover(self._screen)
        if self._currentHoverSurface is not None:
            self._currentHoverSurface.setState("hover")

    def getHover(self, surface):
        hoverSurface = None
        for _, childSurface in surface:
            if not childSurface.isLoaded() or childSurface.isState("disabled") or not childSurface.isSelectable():
                continue

            if childSurface.getFrame().mouseIn():
                nestedChildHover = self.getHover(childSurface)
                hoverSurface = childSurface if nestedChildHover is None else nestedChildHover
            else:
                childSurface.setState("normal")

        return hoverSurface

    @EventHandler(pygame.MOUSEBUTTONDOWN)
    def clickdown(self, event):
        print('click down at', event.pos)

    @EventHandler(pygame.MOUSEBUTTONUP)
    def clickup(self, event):
        if self._currentHoverSurface is not None:
            self._currentHoverSurface.runActions()
        print('click up at', event.pos)
    
    @EventHandler(pygame.KEYDOWN)
    def keydown(self, event):
        pass
        
    @EventHandler(pygame.KEYUP)
    def keyup(self, event):
        pass
    
    @EventHandler(pygame.QUIT)
    def quit(self, event):
        pygame.quit()
        exit()