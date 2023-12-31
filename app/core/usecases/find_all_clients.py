from typing import List, Optional

from pydantic import BaseModel

from app.core.ports.client_repository import ClientRepository
from app.core.models.client import Client


class FindAllClientsCommand(BaseModel):
    issuer: Optional[str] = None


class FindAllClientsHandler:
    def __init__(self, client_repository: ClientRepository):
        self.client_repository = client_repository

    def __call__(self, command: FindAllClientsCommand) -> List[Client]:
        if command.issuer:
            return [self.client_repository.of_issuer(issuer=command.issuer)]

        return self.client_repository.find_all()
