class Client:
    def __init__(
        self,
        id: str,  # Cozy client id
        issuer: str,  # Cozy instance url
        name: str,  # Cozy client name
        secret: str,  # Cozy client secret
        registration_access_token: str,  # Cozy client registration access token
        access_token: str = None,
        refresh_token: str = None,
    ) -> None:
        self.id = id
        self.issuer = issuer
        self.name = name
        self.secret = secret
        self.registration_access_token = registration_access_token
        self.access_token = access_token
        self.refresh_token = refresh_token

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Client):
            return self.id == value.id
        return False
