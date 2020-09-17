class Container:
    def __init__(self, container=None):
        if container == None or type(container) != dict:
            self.container = dict()
        else:
            self.container = container
    
    def __iter__(self):
        self.counter = 0
        return self

    def __next__(self):
        if self.counter >= len(self.container):
            self.counter = 0
            raise StopIteration

        current = getattr(self, self.container[self.counter])
        self.counter += 1
        return current