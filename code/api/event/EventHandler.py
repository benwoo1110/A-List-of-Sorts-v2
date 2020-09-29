class EventHandler(object):

    def __init__(self, evenType):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.eventType = evenType

    def __call__(self, func):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """
        def wrappedFunc(funcSelf, event, *args, **kwargs):
            if self.eventType == event.type:
                func(funcSelf, event, *args, **kwargs)
        return wrappedFunc