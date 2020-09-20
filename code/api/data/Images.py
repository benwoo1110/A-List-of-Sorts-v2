import pygame
import glob

from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.utils.File import File


class Images(Container):
    def __init__(self, imageFolder:File, frame:Frame, fileType:str = '*.png'):
        super().__init__()
        self._imageFolder = imageFolder
        self._fileType = fileType
        self._frame = frame

    def setUp(self, surface):
        self._surface = surface

        # get the image
        imageDict = self._imageFolder.getContainingFiles(self._fileType)
        for imageFileName, imageFile in imageDict.items():
            # Get name
            imageName = imageFileName.split('.')[0]
            # Load image
            loadedImage = pygame.image.load(imageFile.getPath()).convert_alpha()
            # Store image
            self.addObject(imageName, loadedImage)

        return self
    
    def load(self, name):
        self._surface.getScreen().blit(self.getImage(name), self._frame.getCoord())

    def loadWithState(self):
        self._surface.getScreen().blit(self.getImage(self._surface.getState()), self._frame.getCoord())

    def setImageFolder(self, folder:File):
        if self.hasImageFolder():
            raise Exception()
        self._imageFolder = folder
    
    def hasImageFolder(self):
        return self._imageFolder != None

    def getImageFolder(self):
        return self._imageFolder

    def getImage(self, name):
        return self.getObject(name)

    def getFrame(self):
        return self._frame
