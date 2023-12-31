import json
from datetime import datetime, timedelta
from typing import Any, Optional
from jose import jwt

from app.configuration import settings
from app.core.models.client import Client
from app.core.ports.authenticator import AbstractAuthenticator
from app.core.ports.client_repository import ClientRepository

ALGORITHM = "HS256"


class Authenticator(AbstractAuthenticator):
    def __init__(self, client_repository: ClientRepository) -> None:
        self.client_repository = client_repository
        self.secret_key = settings.app_secret
        super().__init__()

    def authenticate(self, token: str) -> Optional[Client]:
        payload = self.decode_token(token)
        client_id = payload.get("client_id")
        if client_id is None:
            return None
        client = self.client_repository.of_id(client_id)
        return client

    def create_access_token(
        self, subject: dict[str, Any], expires_delta: int = None
    ) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=525600)  # 1 year
        payload = {"exp": expires_delta, "sub": str(subject).replace("'", '"')}
        encoded = jwt.encode(claims=payload, key=self.secret_key, algorithm=ALGORITHM)
        return encoded

    def decode_token(self, token: str) -> dict[str, Any]:
        payload = jwt.decode(token=token, key=self.secret_key, algorithms=ALGORITHM)
        # check if token has expired
        if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            raise Exception("Token has expired")
        # decode payload from string to dict
        sub = payload.get("sub")
        if sub is None:
            raise Exception("Invalid token")
        return json.loads(sub)
