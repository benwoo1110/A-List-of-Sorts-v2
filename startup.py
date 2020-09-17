import os


# Set program evironment
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Dependency checking
from code.api.utils.Dependency import Dependency

with open("./requirements.txt", "r") as requirementsFile:
    packages = requirementsFile.read().split("\n")
Dependency(packages).check()


# App setup
from code.api.App import App
from code.api.utils.Logger import Logger

app = App("A List of Sort")
Logger.get().info("TEST START")