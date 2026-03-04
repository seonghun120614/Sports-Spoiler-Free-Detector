from abc import ABC, abstractmethod

class EntityExtractor(ABC):

    @abstractmethod
    def extract(self, target):
        """extracting labels from target"""
        pass