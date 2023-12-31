from app.core.ports.jwt_provider import JwtProviderInterface
from app.core.ports.client_repository import ClientRepository
from app.core.ports.cozy_client import CozyClientInterface
from app.core.models.client import Client


class GetDocumentsCommand:
    def __init__(self, client_id: str):
        self.client_id = client_id


class GetDocumentsCommandHandler:
    def __init__(
        self,
        cozy_client: CozyClientInterface,
        repository: ClientRepository,
        jwt: JwtProviderInterface,
    ):
        self.cozy_client = cozy_client
        self.repository = repository
        self.jwt = jwt

    def __call__(self, command: GetDocumentsCommand) -> dict[str, any]:
        client = self.repository.of_id(command.client_id)
        if client is None:
            raise Exception(f"Client {command.client_id} not found")
        # get documents
        documents = self._cozy_client.get_documents(client)
        return documents

    def refresh_token(self, client: Client) -> Client:
        client = self.cozy_client.refresh_token(client)
        self.repository.save(client)
        return client
