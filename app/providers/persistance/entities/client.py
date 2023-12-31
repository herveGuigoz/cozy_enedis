import uuid
from sqlalchemy import Column, DateTime, String, Uuid, func
from app.core.models.client import Client
from ..database import Entity


class ClientEntity(Entity):
    __tablename__ = "clients"

    id = Column(String, primary_key=True, index=True)
    issuer = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    registration_access_token = Column(String, nullable=False)
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_model(self) -> Client:
        return Client(
            id=self.id,
            issuer=self.issuer,
            name=self.name,
            secret=self.secret,
            registration_access_token=self.registration_access_token,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
        )

    @staticmethod
    def from_model(client: Client) -> "ClientEntity":
        return ClientEntity(
            id=client.id,
            issuer=client.issuer,
            name=client.name,
            secret=client.secret,
            registration_access_token=client.registration_access_token,
            access_token=client.access_token,
            refresh_token=client.refresh_token,
        )
