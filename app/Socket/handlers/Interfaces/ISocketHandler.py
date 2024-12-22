from abc import ABC, abstractmethod

class ISocketHandler(ABC):
    
    @abstractmethod
    def routes_share_socket_handler(self, data, to: str = None):
        pass

    
