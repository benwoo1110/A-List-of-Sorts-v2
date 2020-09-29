from abc import ABC, abstractmethod


class Action(ABC):
    @abstractmethod
    def do(self):
        pass

class Runclass(Action):
    def __init__(self, run:any, *args, **kwargs):
        if not callable(run):
            raise AttributeError("run needs to be callable!")
        self.run = run
        self.args = args
        self.kwargs = kwargs

    def do(self):
        return self.run(*self.args, **self.kwargs)