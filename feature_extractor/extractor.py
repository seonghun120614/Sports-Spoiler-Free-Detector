from abc import ABC, abstractmethod

"""
Abstract Class

for homogeneity about other feature extractors
"""
class EntityExtractor(ABC):

    @abstractmethod
    def extract(self, target):
        """extracting labels from target"""
        pass