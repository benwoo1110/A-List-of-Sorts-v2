import pygame

from code.api.utils.File import File
from code.api.utils.Logger import Logger


class App:
    RESOURCES_FOLDER = File("./resources/")
    LOGS_FOLDER = File("./logs/")
    CONFIG_FILE = File("./config.yml")

    def __init__(self, name):
        self.name = name

        # Logging
        App.LOGS_FOLDER.createDirIfEmpty()
        Logger.setUp(self.name, 5, "INFO", "DEBUG")

        # Resource
        self.resourceFiles = App.RESOURCES_FOLDER.getContainingFiles()

        # Config
        if not App.CONFIG_FILE.exist():
            self.resourceFiles.get("default_config.yml").copyTo(App.CONFIG_FILE)
        self.configData = App.CONFIG_FILE.loadYaml()

        print(self.configData)
        pygame.init()