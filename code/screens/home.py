from code.api.core.Screen import Screen
from code.api.core.Surface import Surface
from code.api.core.Frame import Frame
from code.api.data.Images import Images
from code.api.data.Text import Text


class home(Screen):
    def __init__(self):
        super().__init__("home")

        self\
        .addSurface(
            Surface(
                name="info",
                type_="button",
                frame=Frame(x=225, y=242, w=751, h=211),
                actions=[]
            )
            .addData("image", Images(None, Frame(x=225, y=242, w=751, h=211)))
            .addChild(
                Surface(
                    name="test",
                    type_="button",
                    frame=Frame(x=225, y=242, w=751, h=211),
                    actions=[]
                )
                .addData("image", Images(None, Frame(x=225, y=242, w=751, h=211)))
                .addData("text", Text(frame=Frame(x=225, y=242, w=751, h=211), text="test"))
            )
        )
    
    def start(self):
        self.getSurface("info").load(withChilds=["test"], nested=True)