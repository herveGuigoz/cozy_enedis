from abc import ABC, abstractmethod
from typing import Optional

from app.core.models.client import Client


class ClientRepository(ABC):
    @abstractmethod
    def of_id(self, id: str) -> Optional[Client]:
        raise NotImplementedError

    @abstractmethod
    def of_issuer(self, issuer: str) -> Optional[Client]:
        raise NotImplementedError

    @abstractmethod
    def find_all(self) -> list[Client]:
        raise NotImplementedError

    @abstractmethod
    def save(self, client: Client) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, client: Client) -> None:
        raise NotImplementedError
