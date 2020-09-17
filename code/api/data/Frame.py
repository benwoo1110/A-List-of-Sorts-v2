import pygame


class Frame:
    windowScale = 1

    @staticmethod
    def setWindowScale(scale:int):
        Frame.windowScale = scale

    def __init__(self, x:int = 0, y:int = 0, w:int = 0, h:int = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def size(self, scale:int = 1) -> tuple:
        return (int(self.w * scale), int(self.h * scale))

    def overlayCoord(self, surfaceCoord:tuple): 
        self.x += surfaceCoord[0]
        self.y += surfaceCoord[1]

    def coord(self, surfaceCoord:tuple = (0, 0), scale:int = 1) -> tuple: 
        return (int((self.x + surfaceCoord[0]) * scale), int((self.y + surfaceCoord[1]) * scale))
    
    def rect(self): return (self.x, self.y, self.w, self.h)

    def move(self, x, y):
        self.x += x
        self.y += y

    def mouseIn(self, surfaceCoord:tuple = (0, 0)) -> bool:
        mousePos = pygame.mouse.get_pos()
        s_x, s_y = surfaceCoord
        return int((self.x + s_x) * Frame.windowScale) < mousePos[0] < int((self.x + self.w + s_x) * Frame.windowScale)\
        and int((self.y + s_y) * Frame.windowScale) < mousePos[1] < int((self.y + self.h + s_y) * Frame.windowScale)