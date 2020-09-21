import  pygame
import os

from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.data.Data import Data
from code.api.data.Images import Images
from code.api.utils.File import File


class Surface(Container):
    def __init__(self, name:str, type_:str, frame:Frame, selectable:bool = True, actions:list = None):
        super().__init__()
        self._name = name
        self._type = type_
        self._frame = frame
        self._selectable = selectable
        self._actions = actions
        self._datas = dict()
        self._state = "normal"
        self._loaded = False

    def setUp(self, parentDir:str, screen):
        self._screen = screen
        self._surfaceDir = os.path.join(parentDir, self._name+"/")

        for data in self._datas.values():
            if (isinstance(data, Images)) and not data.hasImageFolder():
                data.setImageFolder(File(self._surfaceDir))
            data.setUp(self)

        for _, childSurface in self:
            childSurface.setUp(self._surfaceDir, screen)

        self.load()

    def unload(self, withChilds:list = None, nested:bool = False):
        self._loaded = False

        for name, child in self: 
            if name not in withChilds:
                continue
            if nested:
                child.unload(withChilds, nested)
            else:
                child.unload()

    def load(self, withChilds:list = None, nested:bool = False):
        for data in self._datas.values():
            data.loadWithState()

        self._loaded = True

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
        self._screen.display()

    def addData(self, name:str, data:Data):
        if not isinstance(data, Data):
            raise TypeError("Not an instance of Data object.")
        self._datas[name] = data
        return self

    def addChild(self, childSurface):
        if not isinstance(childSurface, Surface):
            raise TypeError("Not an instance of Surface object.")
        self.addObject(childSurface.getName(), childSurface)
        return self

    def setState(self, newState:str):
        self._state = newState
        self.display()

    def isState(self, state:str) -> bool:
        return self._state.lower() == state.lower()

    def getData(self, name) -> Data:
        return self._datas.get(name)

    def listData(self) -> list:
        return self._datas.keys()

    def getChild(self, name:str):
        return self.getObject(name)

    def listChild(self) -> list:
        return self._container.keys()

    def getName(self) -> str:
        return self._name

    def getScreen(self):
        return self._screen.getScreen()

    def getFrame(self) -> Frame:
        return self._frame

    def getType(self) -> str:
        return self._type

    def isSelectable(self) -> bool:
        return self._selectable

    def getState(self) -> str:
        return self._state

    def getActions(self) -> list:
        return self._actions
