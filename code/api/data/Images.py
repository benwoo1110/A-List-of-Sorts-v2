import pygame
import glob

from code.api.core.Container import Container
from code.api.core.Frame import Frame
from code.api.utils.File import File


class Images(Container):
    def __init__(self, imageFolder:File, frame:Frame, fileType:str = '*.png'):
        super().__init__()
        self.imageFolder = imageFolder
        self.fileType = fileType
        self.frame = frame

    def setUp(self, surface):
        self.surface = surface

        # get the image
        imageDict = self.imageFolder.getContainingFiles(self.fileType)
        for imageFileName, imageFile in imageDict.items():
            # Get name
            imageName = imageFileName.split('.')[0]
            # Load image
            loadedImage = pygame.image.load(imageFile.getPath()).convert_alpha()
            # Store image
            self.addContainer(imageName, loadedImage)

        return self

    def getImage(self, name):
        return self.container.get(name)
    
    def load(self, name):
        self.surface.getScreen().blit(self.getImage(name), self.frame.coord())

    def loadWithState(self):
        self.surface.getScreen().blit(self.getImage(self.surface.state), self.frame.coord())