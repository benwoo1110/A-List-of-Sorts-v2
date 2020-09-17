import  pygame
import os

from code.api.core.Screen import Screen
from code.api.core.Window import Window
from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.data.Images import Images
from code.api.utils.File import File


class Surface(Container):
    def __init__(self, name:str, type_:str, frame:Frame, selectable:bool = True, actions:list = None):
        super().__init__()
        self.name = name
        self.type_ = type_
        self.frame = frame
        self.selectable = selectable
        self.actions = actions
        self.datas = dict()
        self.surface = pygame.surface.Surface(self.frame.size(), pygame.SRCALPHA)
        self.state = "normal"
        self.loaded = False

    def setUp(self, parentDir:str, screen:Screen):
        self.screen = screen
        self.surfaceDir = os.path.join(parentDir, self.getName()+"/")

        for data in self.datas.values():
            if (isinstance(data, Images)) and data.imageFolder == None:
                data.imageFolder = File(self.surfaceDir)
            data.setUp(self)

        for _, childSurface in self:
            childSurface.setUp(self.surfaceDir, screen)

        self.load()

    def addData(self, name, data):
        self.datas[name] = data
        return self

    def getData(self, name):
        return self.datas.get(name)

    def addChild(self, childSurface):
        self.addContainer(childSurface.getName(), childSurface)
        return self

    def getChild(self, name:str):
        return self.getContainer(name)

    def listChild(self) -> list:
        return self.container.keys()

    def getName(self):
        return self.name

    def getScreen(self):
        return self.screen.getScreen()

    def load(self, withChilds:list = None, nested:bool = False):
        for data in self.datas.values():
            data.loadWithState()

        self.loaded = True

        if withChilds == None:
            return

        for name, child in self: 
            if name not in withChilds:
                continue
            if nested:
                child.load(withChilds, nested)
            else:
                child.load()

    def display(self, withChilds:list = None, nested:bool = False):        
        self.load(withChilds, nested)
        self.screen.display()