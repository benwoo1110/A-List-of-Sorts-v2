import pygame
import os

from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.core.Window import Window
from code.api.data.Images import Images
from code.api.utils.File import File


class Screen(Container):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.screenDir = os.path.join("./surfaces/", self.getName()+"/")
    
    def start(self):
        pass

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

    def end(self):
        pass

    def setUp(self, frame:Frame, window:Window):
        self.frame = frame
        self.window = window
        self.screen = pygame.surface.Surface(frame.size(), pygame.SRCALPHA)

        self.backgroundImage = Images(File(self.screenDir), self.frame).setUp(None)
        self.screen.blit(self.backgroundImage.getImage('background'), self.backgroundImage.frame.getCoord())

        for _, surface in self:
            surface.setUp(self.screenDir, self)

    def addSurface(self, surface):
        self.addContainer(surface.getName(), surface)
        return self

    def getSurface(self, name:str):
        return self.container.get(name)
    
    def getScreen(self):
        return self.screen

    def getName(self):
        return self.name

    def display(self):
        self.window.triggerUpdate()