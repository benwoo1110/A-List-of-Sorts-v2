import os
import glob
import yaml
import shutil

from code.api.utils.Logger import Logger


class File:
    def __init__(self, filepath):
        self.filepath = os.path.join(filepath)

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

    def getContainingFiles(self, filter_:str = "*", withExtension:bool = True, fileObject:bool = True) -> dict:
        files = dict()
        for file_ in glob.glob(os.path.join(self.filepath, filter_)):
            if not os.path.isfile(file_):
                continue
            files[File.getFileName(file_, withExtension)] = File(file_) if fileObject else file_
        return files

    def getName(self, withExtension:bool = True):
        return File.getFileName(self.filepath, withExtension)

    @staticmethod
    def getFileName(filepath:str, withExtension:bool = True):
        if not os.path.isfile(filepath):
            raise AttributeError("Path '{}' is not a file!".format(filepath))
        fileName = os.path.basename(filepath)
        return fileName if withExtension else fileName.split(".")[0]

    def copyTo(self, dst) -> bool:
        try:
            shutil.copyfile(self.filepath, dst.filepath)
        except Exception as e:
            Logger.get().error("Error copying file", exc_info=True)

    def getPath(self) -> str:
        return self.filepath

    def __repr__(self):
        return "File('{}')".format(self.getPath())