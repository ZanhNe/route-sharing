from abc import ABC, abstractmethod
from typing import List

class IRedisService(ABC):

    @abstractmethod
    def set_value(self, key, value):
        pass

    @abstractmethod
    def get_value(self, key):
        pass

    @abstractmethod
    def start_subsrcibe(self, channels: List[str]):
        pass