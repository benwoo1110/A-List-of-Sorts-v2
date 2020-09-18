# Set program evironment
import os

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
from code.api.data.Text import TextFormat
from code.api.utils.File import File
from code.screens.home import home

app = App(name="A List of Sort v2", size=(1024, 768))

TextFormat.setDefaultFont(TextFormat.getCustomFont("Futura"))

app.registerScreen(home())

Logger.get().info("START")
app.start("home")