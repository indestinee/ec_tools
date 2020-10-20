import abc


class CacheInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def items(self):
        pass

    @abc.abstractmethod
    def remove(self, name):
        pass

    @abc.abstractmethod
    def dump(self, data, name):
        pass

    @abc.abstractmethod
    def load(self, name):
        pass
