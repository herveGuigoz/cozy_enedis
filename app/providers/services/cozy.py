import requests
from urllib.parse import quote, urlencode, urljoin

from app.configuration import settings
from app.core.exceptions.exceptions import UnauthorizedError
from app.core.models.client import Client
from app.core.ports.cozy_client import CozyClientInterface


class Cozyclient(CozyClientInterface):
    def __init__(self):
        entrypoint = settings.public_entrypoint
        self.public_entrypoint = (
            entrypoint[:-1] if entrypoint.endswith("/") else entrypoint
        )
        self.scopes = [
            "io.cozy.apps",
            "io.cozy.oauth.clients",
            "com.grandlyon.ecolyo.*",
            "com.grandlyon.enedis.*",
            "com.grandlyon.grdf.*",
            "com.grandlyon.egl.*",
        ]
        self.session = requests.Session()

    def register(
        self,
        issuer: str,
        client_name: str,
        software_id: str,
        redirect_uri: str,
    ) -> Client:
        payload = {
            "client_name": client_name,
            "software_id": software_id,
            "redirect_uris": [redirect_uri],
        }
        try:
            endpoint = urljoin(issuer, "/auth/register")
            # Send the request to the server to register the client
            response = self.session.post(url=endpoint, json=payload)
            # Raise an exception if the request failed
            response.raise_for_status()
            body = response.json()
            return Client(
                id=body["client_id"],
                issuer=issuer,
                name=body["client_name"],
                secret=body["client_secret"],
                registration_access_token=body["registration_access_token"],
            )
        except Exception as exception:
            raise Exception(f"Failed to register client: {exception}")

    def unregister(self, client: Client) -> None:
        try:
            endpoint = urljoin(client.issuer, f"/auth/register/{client.id}")
            headers = {"Authorization": f"Bearer {client.registration_access_token}"}
            response = self.session.delete(url=endpoint, headers=headers)
            response.raise_for_status()
        except Exception as exception:
            raise Exception(f"Failed to unregister client: {exception}")

    def get_authorization_url(
        self, client: Client, redirect_uri: str, state: str
    ) -> str:
        params = {
            "client_id": client.id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "state": state,
        }
        return urljoin(client.issuer, "/auth/authorize") + "?" + urlencode(params)

    def get_access_token(self, client: Client, code: str) -> Client:
        try:
            endpoint = urljoin(client.issuer, "/auth/access_token")
            payload = {
                "client_id": client.id,
                "client_secret": client.secret,
                "code": code,
                "grant_type": "authorization_code",
            }
            response = self.session.post(url=endpoint, data=payload)
            response.raise_for_status()
            data = response.json()
            # Update the client access token and refresh token
            client.access_token = data["access_token"]
            client.refresh_token = data["refresh_token"]
            return client
        except Exception as exception:
            raise Exception(f"Failed to get access token: {exception}")

    def refresh_token(self, client: Client) -> Client:
        try:
            endpoint = urljoin(client.issuer, "/auth/access_token")
            payload = {
                "client_id": client.id,
                "client_secret": client.secret,
                "refresh_token": client.refresh_token,
                "grant_type": "refresh_token",
            }
            response = self.session.post(url=endpoint, data=payload)
            # Raise an exception if the request failed
            response.raise_for_status()
            # Updaete the client access token
            data = response.json()
            client.access_token = data["access_token"]
            return client
        except Exception as exception:
            raise Exception(f"Failed to refresh access token: {exception}")

    def get_document(self, client: Client, doctype: str, limit: int) -> dict:
        headers = {"Authorization": f"Bearer {client.access_token}"}
        url = f"{client.issuer}/data/com.grandlyon.enedis.{doctype}/_all_docs?include_docs=true&limit=${limit}"
        response = self.session.get(url, headers=headers)
        # Raise an exception if the token is invalid
        if response.status_code == 401:
            raise UnauthorizedError()
        # Raise an exception if the request failed
        response.raise_for_status()

        return response.json()
