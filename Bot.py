from abc import ABC, abstractmethod, abstractproperty

class Bot(ABC):

    def __init__(self, database):
        self.database = database

    @abstractmethod
    def fetch_updates(self):
        pass

    @abstractmethod
    def get_all_items(self) :
        pass
