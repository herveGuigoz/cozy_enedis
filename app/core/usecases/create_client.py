import secrets
from pydantic import BaseModel, HttpUrl

from app.core.ports.jwt_provider import JwtProviderInterface
from app.configuration import settings
from app.core.ports.client_repository import ClientRepository
from app.core.ports.cozy_client import CozyClientInterface
from app.core.models.client import Client
from app.providers.services.files_service import FileService


class CreateClientCommand(BaseModel):
    issuer: str  # Cozy instance url
    redirect_uri: str  # Client redirect uri


class ClientCreatedResponse(BaseModel):
    issuer: str
    state: str
    authorization_url: str


class CreateClientCommandHandler:
    def __init__(
        self,
        client_repository: ClientRepository,
        cozy_client: CozyClientInterface,
    ):
        self._client_repository = client_repository
        self._cozy_client = cozy_client

    def __call__(self, command: CreateClientCommand) -> ClientCreatedResponse:
        # Prepare data
        issuer = self.clean_url(command.issuer)
        redirect_uri = self.clean_url(command.redirect_uri)
        # Find or create cozy client
        client = self._client_repository.of_issuer(issuer=issuer)
        # Log the client in if it exists
        if client is not None:
            print(f"Client {client.id} already exists")
        if client is None:
            print(f"Creating client for {issuer}")
            client = self._cozy_client.register(
                issuer=issuer,
                client_name=settings.client_name,
                software_id=settings.software_id,
                redirect_uri=redirect_uri,
            )
            self._client_repository.save(client)
        # Build the authorization url
        state = secrets.token_urlsafe(16)
        authorization_url = self._cozy_client.get_authorization_url(
            client=client,
            redirect_uri=redirect_uri,
            state=state,
        )

        return ClientCreatedResponse(
            issuer=issuer,
            state=state,
            authorization_url=authorization_url,
        )

    def clean_url(self, url: str) -> str:
        return url[:-1] if url.endswith("/") else url

    def debug(self, command: CreateClientCommand) -> ClientCreatedResponse:
        issuer = self.clean_url(command.issuer)
        redirect_uri = self.clean_url(command.redirect_uri)
        # Find or create cozy client
        body = FileService.read("etc/client.json")
        client = Client(
            id=body["client_id"],
            issuer=issuer,
            name=body["client_name"],
            secret=body["client_secret"],
            registration_access_token=body["registration_access_token"],
        )
        self._client_repository.save(client)
        # Build the authorization url
        state = secrets.token_urlsafe(16)
        authorization_url = self._cozy_client.get_authorization_url(
            client=client,
            redirect_uri=redirect_uri,
            state=state,
        )

        return ClientCreatedResponse(
            issuer=client.issuer,
            state=state,
            authorization_url=authorization_url,
        )
