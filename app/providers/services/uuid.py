import uuid

from app.core.ports.uuid_provider import UuidProviderInterface


class UuidProvider(UuidProviderInterface):
    def generate(self) -> str:
        return uuid.uuid4()
