from typing import Dict, Type, Any
class BaseDIContainer():
    def __init__(self) -> None:
        self.container: Dict[Type, Any] = {}
    def register_container(self, interface: Type, implementation: Type):
        self.container[interface] = implementation
    def resolve(self, interface: Type):
        if (not interface in self.container):
            raise ValueError(f'Interface {interface} not registered')
        return self.container[interface]


class RepositoryDIContainer(BaseDIContainer):
    def __init__(self) -> None:
        super().__init__()

class ServiceDIContainer(BaseDIContainer):
    def __init__(self) -> None:
        super().__init__()