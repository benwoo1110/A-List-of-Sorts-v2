from abc import ABC, abstractmethod

from code.api.core.Frame import Frame


class Data(ABC):
    @abstractmethod
    def setUp(self, surface):
        pass

    @abstractmethod
    def loadWithState(self):
        pass

    @abstractmethod
    def getFrame(self) -> Frame:
        pass