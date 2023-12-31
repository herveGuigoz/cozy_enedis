from typing import Optional
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound

from app.core.models.client import Client
from app.core.ports.client_repository import ClientRepository

from ..entities.client import ClientEntity


class AlchemyClientRepository(ClientRepository):
    def __init__(self, session: Session):
        self.session: Session = session

    def of_id(self, id: str) -> Optional[Client]:
        try:
            instance = self.session.query(ClientEntity).filter_by(id=id).first()
            if not instance:
                return None
            return instance.to_model()
        except:
            raise

    def of_issuer(self, issuer: str) -> Optional[Client]:
        try:
            instance = self.session.query(ClientEntity).filter_by(issuer=issuer).first()
            if not instance:
                return None
            return instance.to_model()
        except:
            raise

    def find_all(self) -> list[Client]:
        try:
            instances = self.session.query(ClientEntity).all()
            return list(map(lambda instance: instance.to_model(), instances))
        except:
            raise

    def save(self, client: Client) -> None:
        try:
            # Try to retrieve an existing client by ID
            q = self.session.query(ClientEntity).filter_by(id=client.id)
            instance = q.one()
            assert isinstance(instance, ClientEntity)
            instance.access_token = client.access_token
            instance.refresh_token = client.refresh_token
            self.session.merge(instance)
        except NoResultFound:
            # If not found, add a new ClientEntity to the session
            self.session.add(ClientEntity.from_model(client))
        # Flush the session to ensure all operations are sent to the database
        self.session.commit()

    def delete(self, client: Client) -> None:
        try:
            self.session.query(ClientEntity).filter_by(id=client.id).delete()
            self.session.commit()
        except:
            raise
