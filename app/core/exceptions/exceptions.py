class ClientAlreadyExistError(Exception):
    def __init__(self, message: str = None):
        self.message = message or "Client already exist"


class ClientDoesNotExistError(Exception):
    def __init__(self, message: str = None):
        self.message = message or "Client does not exist"


class UnauthorizedError(Exception):
    def __init__(self, message: str = None):
        self.message = message or "Token is invalid or expired"
