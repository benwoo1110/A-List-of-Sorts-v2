import pygame

from code.api.core.Frame import Frame
from code.api.core.Window import Window
from code.api.core.Screen import Screen
from code.api.data.Text import TextFormat
from code.api.utils.File import File
from code.api.utils.Logger import Logger


class App:
    pygame.init()

    FONTS_FOLDER = File("./fonts/")
    RESOURCES_FOLDER = File("./resources/")
    LOGS_FOLDER = File("./logs/")
    CONFIG_FILE = File("./config.yml")

    def __init__(self, name:str, size:tuple):
        self.name = name
        self.frame = Frame(w=size[0], h=size[1])

        # Config
        if not App.CONFIG_FILE.exist():
            self.resourceFiles.get("default_config.yml").copyTo(App.CONFIG_FILE)
        self.configData = App.CONFIG_FILE.loadYaml()

        # Logging
        App.LOGS_FOLDER.createDirIfEmpty()
        Logger.setUp(self.name, 5, "INFO", "DEBUG")

        # Resource
        self.resourceFiles = App.RESOURCES_FOLDER.getContainingFiles()

        # Font
        TextFormat.addCustomFonts(App.FONTS_FOLDER.getContainingFiles(withExtension=False, fileObject=False))

        # Window
        self.window = Window(self.getResource("icon.png"), self.getName(), False, 1, size)

    def registerScreen(self, screen:Screen):
        screen.setUp(self.frame, self.window)
        self.window.addScreen(screen)

    def start(self, startScreen):
        self.window.mainloop(startScreen)

    def getName(self) -> str:
        return self.name

    def getFrame(self) -> Frame:
        return self.frame

    def getResource(self, name) -> File:
        return self.resourceFiles.get(name)