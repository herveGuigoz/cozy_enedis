import requests
from pydantic import BaseModel


class KeycloakUser(BaseModel):
    sub: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: str


class KeycloakError(Exception):
    def __init__(self, status_code: int, reason: str):
        self.status_code = status_code
        self.reason = reason
        super().__init__(f"HTTP {status_code}: {reason}")


class Keycloak:
    def __init__(self, server_url: str, client_id: str, client_secret: str):
        self.server_url = server_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()

    def userinfo(self, token: str) -> KeycloakUser:
        response = self.session.get(
            url=f"{self.server_url}/protocol/openid-connect/userinfo",
            headers={"Authorization": f"Bearer {token}"},
        )
        status_code = response.status_code
        if status_code == 200:
            return KeycloakUser(**response.json())
        if status_code == 401:
            raise KeycloakError(status_code=401, reason="Unauthorized")
        else:
            raise KeycloakError(status_code=status_code, reason=response.json())
