from datetime import datetime, timedelta
from typing import Any
from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWTClaimsError

from app.configuration import settings
from app.core.ports.jwt_provider import JwtProviderInterface

ALGORITHM = "HS256"


class JwtProvider(JwtProviderInterface):
    def __init__(self):
        self.key = settings.app_secret

    def encode(self, payload: dict[str, Any], expires_delta: int = None) -> str:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta
        else:
            expires_delta = datetime.utcnow() + timedelta(minutes=525600)  # 1 year
        payload = {"exp": expires_delta, "sub": str(payload).replace("'", '"')}
        encoded = jwt.encode(claims=payload, key=self.key, algorithm=ALGORITHM)
        return encoded

    def decode(self, token: str, verify: bool = True) -> dict[str, any]:
        payload = jwt.decode(
            token=token,
            key=self.key,
            algorithms=ALGORITHM,
            options={"verify_signature": verify, "verify_aud": verify},
        )
        return payload

    def token_is_valid(self, token: str) -> bool:
        try:
            self.decode(token=token, verify=False)
            return True
        except (ExpiredSignatureError, JWTError, JWTClaimsError):
            return False
