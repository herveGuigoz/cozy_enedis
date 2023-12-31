from abc import ABC, abstractmethod


class JwtProviderInterface(ABC):
    @abstractmethod
    def encode(self, payload: dict) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode(self, token: str, verify: bool = True) -> dict:
        raise NotImplementedError

    @abstractmethod
    def token_is_valid(self, token: str) -> bool:
        raise NotImplementedError
