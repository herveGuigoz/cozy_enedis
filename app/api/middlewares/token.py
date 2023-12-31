from fastapi import Depends
from api.app.core.exceptions.exceptions import UnauthorizedError
from app.core.ports.client_repository import ClientRepository
from app.providers.dependencies import client_repository, cozy_client
from app.core.ports.cozy_client import CozyClientInterface


def request_new_token(
    client_id: str,
    cozy: CozyClientInterface = Depends(cozy_client),
    repository: ClientRepository = Depends(client_repository),
) -> None:
    client = repository.of_id(client_id)
    if client is None:
        raise Exception(f"Client {client_id} not found")
    client = cozy.refresh_token(client)
    repository.save(client)
    return


def renew_access_token(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except UnauthorizedError:
            # Invoke the code responsible for get a new token
            request_new_token(client_id=kwargs["client_id"])
            # once the token is refreshed, we can retry the operation
            return func(*args, **kwargs)

    return wrapper
