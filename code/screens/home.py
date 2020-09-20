from code.api.core.Screen import Screen
from code.api.core.Surface import Surface
from code.api.core.Frame import Frame
from code.api.data.Images import Images
from code.api.data.Text import Text, TextFormat


class home(Screen):
    def __init__(self):
        super().__init__("home")

        self\
        .addSurface(
            Surface(
                name="type",
                type_="button",
                frame=Frame(x=246, y=149, w=729, h=70),
                actions=[]
            )
            .addData("image", Images(None, Frame(x=246, y=149, w=729, h=70)))
            .addData("text", Text(
                frame=Frame(x=271, y=159, w=628, h=53),
                text="Insertion sort",
                format_=TextFormat(fontSize=38, pos="center")
            ))
        )\
        .addSurface(
            Surface(
                name="info",
                type_="button",
                frame=Frame(x=225, y=242, w=751, h=211),
                actions=[]
            )
            .addData("image", Images(None, Frame(x=225, y=242, w=751, h=211)))
            .addData("text", Text(
                frame=Frame(x=252, y=260, w=695, h=168),
                text="Bubble sort, is one of the most simplest sorting algorithm that repeatedly steps through the list, compares adjacent pairs and swaps them if they are in the wrong order.",
                format_=TextFormat(fontSize=31, pos="center", warpText=48)
            ))
        )\
        .addSurface(
            Surface(
                name="speed",
                type_="button",
                frame=Frame(x=271, y=480, w=704, h=70),
                actions=[]
            )
            .addData("image", Images(None, Frame(x=271, y=480, w=704, h=70)))
            .addData("text", Text(
                frame=Frame(x=296, y=490, w=654, h=53),
                text="100.0", suffix=" swaps per sec",
                format_=TextFormat(fontSize=38, pos="center")
            ))
        )\
        .addSurface(
            Surface(
                name="length",
                type_="button",
                frame=Frame(x=403, y=575, w=572, h=70),
                actions=[]
            )
            .addData("image", Images(None, Frame(x=403, y=575, w=572, h=70)))
            .addData("text", Text(
                frame=Frame(x=428, y=585, w=522, h=53),
                text="10", suffix=" bars",
                format_=TextFormat(fontSize=38, pos="center")
            ))
        )\
        .addSurface(
            Surface(
                name="run",
                type_="button",
                frame=Frame(x=781, y=671, w=194, h=70),
                actions=[]
            )
            .addData("image", Images(None, Frame(x=781, y=671, w=194, h=70)))
        )
    
    def start(self):
        pass