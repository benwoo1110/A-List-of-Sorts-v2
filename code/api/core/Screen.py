import pygame

from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.core.Window import Window
from code.api.data.Images import Images
from code.api.utils.File import File


class Screen(Container):
    def __init__(self, name):
        super().__init__()
        self.name = name
    
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
        self.backgroundImage = Images(File("./surfaces/{}".format(self.name)), self.frame).setUp()

        self.screen.blit(self.backgroundImage.getImage('background'), self.backgroundImage.frame.coord())

    def addSurfaces(self, surfaces:list):
        for surface in surfaces:
            self.container[surface.getName()] = surface

    def getSurface(self, name:str):
        return self.container.get(name)
    
    def getScreen(self):
        return self.screen

    def getName(self):
        return self.name

    def display(self):
        self.window.triggerUpdate()