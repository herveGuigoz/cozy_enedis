from pydantic import BaseModel
from app.core.exceptions.exceptions import ClientDoesNotExistError
from app.core.ports.client_repository import ClientRepository
from app.core.ports.cozy_client import CozyClientInterface


class DeleteClientCommand(BaseModel):
    client_id: str


class DeleteClientCommandHandler:
    def __init__(
        self, client_repository: ClientRepository, cozy_client: CozyClientInterface
    ):
        self._client_repository = client_repository
        self._cozy_client = cozy_client

    def __call__(self, command: DeleteClientCommand) -> None:
        # check if client exist
        client = self._client_repository.of_id(command.client_id)
        if client is None:
            raise ClientDoesNotExistError()
        # delete client on cozy server
        self._cozy_client.unregister(client)
        # delete client
        self._client_repository.delete(client)
