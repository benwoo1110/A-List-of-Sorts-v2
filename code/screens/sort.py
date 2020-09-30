from code.api.core.Screen import Screen
from code.api.core.Surface import Surface
from code.api.core.Frame import Frame
from code.api.data.Images import Images
from code.api.data.Text import Text, TextFormat
from code.api.event.Action import Runclass


class sort(Screen):
    def __init__(self):
        super().__init__(name="sort")

        self\
            .addSurface(
                Surface(
                    name="back",
                    type_="button",
                    frame=Frame(x=71, y=41, w=112, h=61),
                    actions=[Runclass(self.switchScreen, "back")]
                )
                .addData("image", Images(None, Frame(x=71, y=41, w=112, h=61)))
            )\
            .addSurface(
                Surface(
                    name="info",
                    type_="button",
                    frame=Frame(x=841, y=41, w=112, h=61),
                    actions=[]
                )
                .addData("image", Images(None, Frame(x=841, y=41, w=112, h=61)))
            )\
            .addSurface(
                Surface(
                    name="stats",
                    type_="container",
                    frame=Frame(x=223, y=606, w=752, h=133),
                    selectable=False,
                    actions=[]
                )
                .addData("image", Images(None, Frame(x=223, y=606, w=752, h=133)))
                .addData("speed", Text(
                    frame=Frame(x=349, y=630, w=254, h=40),
                    text="0", suffix=" swaps per sec",
                    format_=TextFormat(fontSize=28, pos="center", warpText=48)
                ))
                .addData("moves", Text(
                    frame=Frame(x=436, y=677, w=167, h=40),
                    text="0",
                    format_=TextFormat(fontSize=28, pos="center", warpText=48)
                ))
                .addData("time", Text(
                    frame=Frame(x=768, y=630, w=177, h=40),
                    text="0.00", suffix=" sec",
                    format_=TextFormat(fontSize=28, pos="center", warpText=48)
                ))
                .addData("length", Text(
                    frame=Frame(x=759, y=677, w=186, h=40),
                    text="0",
                    format_=TextFormat(fontSize=28, pos="center", warpText=48)
                ))
            )\
            .addSurface(
                Surface(
                    name="sortbox",
                    type_="container",
                    frame=Frame(x=52, y=145, w=922, h=430),
                    selectable=False,
                    actions=[]
                )
                .addData("image", Images(None, Frame(x=52, y=145, w=922, h=430)))
                .addChild(
                    Surface(
                        name="rerun",
                        type_="button",
                        frame=Frame(x=906, y=521, w=68, h=55),
                        selectable=False,
                        actions=[]
                    )
                    .addData("image", Images(None, Frame(x=906, y=521, w=68, h=55)))
                )
            )