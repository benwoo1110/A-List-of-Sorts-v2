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
from code.api.core.Screen import Screen

class testScreen(Screen):
    def __init__(self, name):
        super().__init__(name)

app = App("A List of Sort", (1024, 768))
app.registerScreen(testScreen('testScreen'))
Logger.get().info("TEST START")
app.start('testScreen')