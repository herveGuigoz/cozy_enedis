from abc import ABC, abstractmethod

from app.core.models.client import Client
from app.core.models.doctype import Doctype


class CozyClientInterface(ABC):
    # TODO: move to configuration
    SOFTWARE_ID: str = "homeassistant"
    CLIENT_NAME: str = "homeassistant"
    REDITECT_URI: str = "http://localhost:80/client/register/callback"

    @abstractmethod
    def register(
        self,
        issuer: str,
        client_name: str,
        software_id: str,
        redirect_uri: str,
        owner: str,
    ) -> Client:
        """Register a new client"""
        raise NotImplementedError

    @abstractmethod
    def unregister(self, client: Client) -> None:
        """Unregisters the currenly configured client with the OAuth server."""
        raise NotImplementedError

    @abstractmethod
    def get_authorization_url(
        self, client: Client, redirect_uri: str, state: str
    ) -> str:
        """Generates the URL that the user should be sent to in order to accept the app's permissions."""
        raise NotImplementedError

    @abstractmethod
    def get_access_token(self, client: Client, code: str, state: str) -> Client:
        """Exchanges an access code for an access token."""
        raise NotImplementedError

    def refresh_token(self, client: Client) -> Client:
        """Refreshes an access token."""
        raise NotImplementedError

    @abstractmethod
    def get_document(
        self, client: Client, doctype: Doctype, limit: int
    ) -> dict[str:any]:
        """Get a document from the server"""
        raise NotImplementedError
