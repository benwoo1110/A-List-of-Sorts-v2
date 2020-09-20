class Container:
    def __init__(self, container=None):
        if container == None or type(container) != dict:
            self._container = dict()
        else:
            self._container = container
    
    def __iter__(self):
        return iter(self._container.items())

    def addObject(self, name, object_:object):
        self._container[name] = object_

    def getObject(self, name):
        return self._container.get(name)

    def delete(self, name) -> object:
        return self._container.pop(name)

    def clearAll(self):
        self._container.clear()
