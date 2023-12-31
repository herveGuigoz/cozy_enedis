from pydantic import BaseModel

from app.core.models.client import Client
from app.core.ports.client_repository import ClientRepository
from app.core.ports.cozy_client import CozyClientInterface
from app.core.ports.jwt_provider import JwtProviderInterface


class AuthorizeClientCommand(BaseModel):
    issuer: str
    code: str


class AuthorizeClientCommandHandler:
    def __init__(
        self,
        client_repository: ClientRepository,
        cozy_client: CozyClientInterface,
    ):
        self._client_repository = client_repository
        self._cozy_client = cozy_client

    def __call__(self, command: AuthorizeClientCommand) -> Client:
        # get client from issuer
        client = self._client_repository.of_issuer(command.issuer)
        if client is None:
            raise Exception("Client not found")
        # get access token from code
        client = self._cozy_client.get_access_token(
            client=client,
            code=command.code,
        )
        # save client
        self._client_repository.save(client)

        return client
