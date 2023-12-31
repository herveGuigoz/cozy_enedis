from typing import Generic, TypeVar
from pydantic import BaseModel, HttpUrl

# T = TypeVar('T')

# class Collection(Generic[T], BaseModel):
#     items: list[T]
#     totalItems: int


class CreateClientRequest(BaseModel):
    issuer: HttpUrl
    redirect_uri: HttpUrl


class CozyClientResponse(BaseModel):
    id: str
    issuer: HttpUrl
    name: str


class ClientAutorizedResponse(BaseModel):
    client_id: str
    client_name: str
