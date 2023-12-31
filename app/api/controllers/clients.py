import re

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Security
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.api.dtos.security import (
    CreateClientRequest,
    CozyClientResponse,
)
from app.api.middlewares.security import get_current_user
from app.core.models.client import Client
from app.core.usecases.find_all_clients import (
    FindAllClientsHandler,
    FindAllClientsCommand,
)
from app.core.usecases.authorize_client import (
    AuthorizeClientCommand,
    AuthorizeClientCommandHandler,
)
from app.core.usecases.create_client import (
    ClientCreatedResponse,
    CreateClientCommand,
    CreateClientCommandHandler,
)
from app.core.usecases.delete_client import (
    DeleteClientCommand,
    DeleteClientCommandHandler,
)
from app.providers.services.keycloak import KeycloakUser
from ...providers.dependencies import (
    authorize_client_usecase,
    create_client_usecase,
    delete_client_usecase,
    dependencies,
    find_all_clients_usecase,
)


router = APIRouter(
    tags=["Clients"],
    dependencies=dependencies,
)

# --------------------------------------------------------------------------------
# Templates
# --------------------------------------------------------------------------------
templates = Jinja2Templates(directory=str("/code/app/templates"))


# --------------------------------------------------------------------------------
# Validators
# --------------------------------------------------------------------------------
def validate_issuer(issuer: str) -> bool:
    pattern = r"^https://[a-zA-Z0-9-]+\.cozygrandlyon\.cloud$"
    return re.match(pattern, issuer) is not None


# --------------------------------------------------------------------------------
# Utils
# --------------------------------------------------------------------------------
# Redirect url to send to the cozy instance
def get_redirect_uri(request: Request) -> str:
    base_url = str(request.base_url)
    uri = router.url_path_for("authorize_callback")
    return f"{base_url.rstrip('/')}{uri}"


# --------------------------------------------------------------------------------
# Controllers
# --------------------------------------------------------------------------------
# Render form template to register a new client
@router.get("/clients/register", name="client_register", include_in_schema=False)
async def register_form(
    request: Request,
) -> dict:
    return templates.TemplateResponse(
        "/cozy_client/register.html", {"request": request}
    )


# Handle form submission to register a new client.
@router.post("/clients/register", name="client_new", include_in_schema=False)
async def register_client(
    request: Request,
    issuer: str = Form(),
    handler: CreateClientCommandHandler = Depends(create_client_usecase),
) -> RedirectResponse:
    # Validate issuer
    if not validate_issuer(issuer):
        raise HTTPException(status_code=400, detail="Invalid issuer")
    # Authorization url to send to the cozy instance
    redirect_uri = get_redirect_uri(request)
    # Create client
    try:
        command = CreateClientCommand(issuer=issuer, redirect_uri=redirect_uri)
        result = handler(command)
        # Store the state & issuer in session or cookie for later validation
        request.session["oauth_state"] = result.state
        request.session["oauth_issuer"] = result.issuer

        return RedirectResponse(url=result.authorization_url, status_code=302)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Callback from the cozy instance after the client has been authorized.
@router.get(
    "/clients/authorize/callback", name="authorize_callback", include_in_schema=False
)
async def authorize_callback(
    code: str,
    state: str,
    request: Request,
    handler: AuthorizeClientCommandHandler = Depends(authorize_client_usecase),
) -> RedirectResponse:
    try:
        # Validate state
        if state != request.session.get("oauth_state"):
            raise HTTPException(status_code=400, detail="Invalid state")
        # Issuer from session
        issuer = request.session.get("oauth_issuer")
        handler(AuthorizeClientCommand(issuer=issuer, code=code))

        return RedirectResponse(url="/docs", status_code=302)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# List all clients registered in our application.
@router.get(
    "/clients",
    response_model=list[CozyClientResponse],
    status_code=200,
    summary="List clients",
    description="List all clients registered in our application",
)
async def list_clients(
    # _: Annotated[KeycloakUser, Security(get_current_user)],
    issuer: str = None,
    handler: FindAllClientsHandler = Depends(find_all_clients_usecase),
) -> list[Client]:
    try:
        command = FindAllClientsCommand(issuer=issuer)
        clients = handler(command)

        return [
            CozyClientResponse(id=client.id, issuer=client.issuer, name=client.name)
            for client in clients
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Delete a client.
@router.delete(
    "/clients/{client_id}",
    status_code=204,
    summary="Delete client",
    description="Delete the client from the cozy instance",
)
async def unregister(
    # _: Annotated[KeycloakUser, Security(get_current_user)],
    client_id: str,
    handler: DeleteClientCommandHandler = Depends(delete_client_usecase),
) -> None:
    return handler(DeleteClientCommand(client_id=client_id))
