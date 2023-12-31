from abc import ABC, abstractmethod


class UuidProviderInterface(ABC):
    @abstractmethod
    def generate(self) -> str:
        raise NotImplementedError
