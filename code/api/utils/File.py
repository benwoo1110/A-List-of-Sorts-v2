import os
import glob
import yaml
import shutil

from code.api.utils.Logger import Logger


class File:
    def __init__(self, filepath):
        self.filepath = filepath

    def createDirIfEmpty(self) -> bool:
        if os.path.isdir(self.filepath):
            return True
        try:
            os.mkdir(self.filepath)
        except Exception as e:
            Logger.get().error(e, exc_info=True)
            return False
        return True

    def loadYaml(self) -> dict:
        # Read from config file
        with open(self.filepath, "r") as yamlFile:
            return yaml.load(yamlFile, Loader=yaml.FullLoader)

    def exist(self) -> bool:
        return os.path.exists(self.filepath)

    def getContainingFiles(self) -> dict:
        files = dict()
        for file_ in glob.glob(os.path.join(self.filepath, "*")):
            files[os.path.basename(file_)] = File(file_)
        return files

    def copyTo(self, dst) -> bool:
        try:
            shutil.copyfile(self.filepath, dst.filepath)
        except Exception as e:
            Logger.get().error("Error copying file", exc_info=True)

    def getPath(self) -> str:
        return self.filepath