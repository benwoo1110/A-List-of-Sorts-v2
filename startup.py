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
from code.api.data.Images import Images
from code.api.utils.File import File


class home(Screen):
    def __init__(self):
        super().__init__('home')


image = Images(File("./surfaces/home/"), None)
test = home()

app = App("A List of Sort", (1024, 768))
image.setUp()

for i in image:
    print(i)

app.registerScreen(test)
Logger.get().info("TEST START")
app.start('home')