class Container:
    def __init__(self, container=None):
        if container == None or type(container) != dict:
            self.container = dict()
        else:
            self.container = container
    
    def __iter__(self):
        return iter(self.container.items())

    def addContainer(self, name, object_:object):
        self.container[name] = object_

    def getContainer(self, name):
        return self.container.get(name)