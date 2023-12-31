from abc import ABC, abstractmethod
from typing import Any, Optional, Union

from ..models.client import Client


class AbstractAuthenticator(ABC):
    @abstractmethod
    def authenticate(self, token: str) -> Optional[Client]:
        raise NotImplementedError

    @abstractmethod
    def create_access_token(
        self, subject: dict[str, Any], expires_delta: int = None
    ) -> str:
        raise NotImplementedError

    @abstractmethod
    def decode_token(self, token: str) -> dict[str, Any]:
        raise NotImplementedError
