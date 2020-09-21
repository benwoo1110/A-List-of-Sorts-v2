import pygame
import os

from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.core.Surface import Surface
from code.api.data.Images import Images
from code.api.utils.File import File


class Screen(Container):
    def __init__(self, name):
        super().__init__()
        self._name = name
        self._screenDir = os.path.join("./surfaces/", self._name+"/")
    
    def start(self):
        pass

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
    
    def end(self):
        pass

    def setUp(self, frame:Frame, window):
        self._frame = frame
        self._window = window
        self._screen = pygame.surface.Surface(frame.size(), pygame.SRCALPHA)

        self._backgroundImage = Images(File(self._screenDir), self._frame).setUp(None)
        self._screen.blit(self._backgroundImage.getImage('background'), self._backgroundImage.getFrame().getCoord())

        for _, surface in self:
            surface.setUp(self._screenDir, self)

    def display(self):
        self._window.triggerUpdate()

    def addSurface(self, surface):
        self.addObject(surface.getName(), surface)
        return self

    def getSurface(self, name:str) -> Surface:
        return self.getObject(name)
    
    def getScreen(self):
        return self._screen

    def getName(self):
        return self._name

    def getFrame(self):
        return self._frame
