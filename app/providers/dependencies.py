from functools import lru_cache
from typing import Iterator
from fastapi import Depends
from pydantic_settings import BaseSettings
from sqlalchemy.orm import Session

from app.core.usecases.get_documents import GetDocumentsCommandHandler
from app.core.ports.jwt_provider import JwtProviderInterface
from app.providers.services.jwt import JwtProvider
from app.core.usecases.find_all_clients import FindAllClientsHandler
from app.core.ports.authenticator import AbstractAuthenticator
from app.core.ports.client_repository import ClientRepository
from app.core.ports.cozy_client import CozyClientInterface
from app.core.ports.uuid_provider import UuidProviderInterface
from app.core.usecases.authorize_client import AuthorizeClientCommandHandler
from app.providers.persistance.repositories.client_repository import (
    AlchemyClientRepository,
)
from app.providers.services.authenticator import Authenticator
from app.providers.services.cozy import Cozyclient
from app.providers.persistance.database import SessionLocal
from app.core.usecases.create_client import (
    CreateClientCommandHandler,
)
from app.core.usecases.delete_client import (
    DeleteClientCommandHandler,
)
from app.providers.services.uuid import UuidProvider


class Settings(BaseSettings):
    app_secret: str


@lru_cache()
def get_settings():
    return Settings()


def database() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def uuid_provider() -> UuidProviderInterface:
    return UuidProvider()


def jwt_provider() -> JwtProviderInterface:
    return JwtProvider()


def cozy_client() -> CozyClientInterface:
    return Cozyclient()


def client_repository(session: Session = Depends(database)) -> ClientRepository:
    return AlchemyClientRepository(session)


def create_client_usecase(
    client_repository: ClientRepository = Depends(client_repository),
    cozy_client: CozyClientInterface = Depends(cozy_client),
) -> CreateClientCommandHandler:
    return CreateClientCommandHandler(
        client_repository=client_repository,
        cozy_client=cozy_client,
    )


def authorize_client_usecase(
    client_repository: ClientRepository = Depends(client_repository),
    cozy_client: CozyClientInterface = Depends(cozy_client),
) -> AuthorizeClientCommandHandler:
    return AuthorizeClientCommandHandler(
        client_repository=client_repository,
        cozy_client=cozy_client,
    )


def find_all_clients_usecase(
    client_repository: ClientRepository = Depends(client_repository),
) -> FindAllClientsHandler:
    return FindAllClientsHandler(client_repository)


def delete_client_usecase(
    client_repository: ClientRepository = Depends(client_repository),
    cozy_client: CozyClientInterface = Depends(cozy_client),
) -> DeleteClientCommandHandler:
    return DeleteClientCommandHandler(client_repository, cozy_client)


def get_documents_usecase(
    cozy_client: CozyClientInterface = Depends(cozy_client),
    client_repository: ClientRepository = Depends(client_repository),
    jwt: JwtProviderInterface = Depends(jwt_provider),
) -> GetDocumentsCommandHandler:
    return GetDocumentsCommandHandler(
        cozy_client=cozy_client, repository=client_repository, jwt=jwt
    )


dependencies = [
    # Database
    Depends(database),
    # Usecases
    Depends(create_client_usecase),
    Depends(find_all_clients_usecase),
    Depends(delete_client_usecase),
    # Repositories
    Depends(client_repository),
    # Cozy
    Depends(cozy_client),
    # Misc
    Depends(uuid_provider),
    Depends(jwt_provider),
]
