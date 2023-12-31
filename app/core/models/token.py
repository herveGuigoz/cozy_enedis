from jose import jwt
from datetime import datetime


class AccessToken:
    def __init__(self, token: str):
        self._token = token
        self._decoded_token = self._decode_token(token)

    def _decode_token(self, token: str):
        try:
            return jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            raise ValueError("Invalid token")

    def is_expired(self):
        exp_timestamp = self._decoded_token.get("exp")
        if exp_timestamp is None:
            raise ValueError("Token has no expiration claim")
        expiration_datetime = datetime.utcfromtimestamp(exp_timestamp)
        return expiration_datetime < datetime.utcnow()
