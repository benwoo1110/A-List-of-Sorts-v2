import pygame


class Frame:
    windowScale = 1

    @staticmethod
    def setWindowScale(scale:int):
        Frame.windowScale = scale

    def __init__(self, x:int = 0, y:int = 0, w:int = 0, h:int = 0):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def overlayCoord(self, surfaceCoord:tuple): 
        self._x += surfaceCoord[0]
        self._y += surfaceCoord[1]

    def move(self, x, y):
        self._x += x
        self._y += y

    def mouseIn(self, surfaceCoord:tuple = (0, 0)) -> bool:
        mousePos = pygame.mouse.get_pos()
        sx, sy = surfaceCoord
        return int((self._x + sx) * Frame.windowScale) < mousePos[0] < int((self._x + self._w + sx) * Frame.windowScale)\
        and int((self._y + sy) * Frame.windowScale) < mousePos[1] < int((self._y + self._h + sy) * Frame.windowScale)

    def getCoord(self, surfaceCoord:tuple = (0, 0), scale:int = 1) -> tuple: 
        return (int((self._x + surfaceCoord[0]) * scale), int((self._y + surfaceCoord[1]) * scale))

    def size(self, scale:int = 1) -> tuple:
        return (int(self._w * scale), int(self._h * scale))
    
    def getRect(self, scale:int = 1) -> tuple:
        return (int(self._x * scale), int(self._y * scale), int(self._w * scale), int(self._h * scale))

    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y

    @property
    def w(self) -> int:
        return self._w

    @property
    def h(self) -> int:
        return self._h
