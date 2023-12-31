from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from app.configuration import settings
from app.providers.services.keycloak import Keycloak, KeycloakError, KeycloakUser


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.oidc_server_url}/protocol/openid-connect/token",
)


def _keycloak() -> Keycloak:
    return Keycloak(
        server_url=settings.oidc_server_url_internal,
        client_id=settings.oidc_client_id,
        client_secret=settings.oidc_client_secret,
    )


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    keycloak: Annotated[Keycloak, Depends(_keycloak)],
) -> KeycloakUser:
    try:
        return keycloak.userinfo(token)
    except KeycloakError as e:
        raise HTTPException(status_code=e.status_code, detail=e.reason)


# oauth2_scheme = OAuth2AuthorizationCodeBearer(
#     authorizationUrl="auth/authorize",
#     tokenUrl="auth/access_token",
#     # https://forge.grandlyon.com/web-et-numerique/factory/llle_project/ecolyo/-/blob/dev/manifest.webapp?ref_type=heads
#     scopes={
#         "com.grandlyon.ecolyo.read": "Analysis of your ecolyo application",
#         "com.grandlyon.enedis.read": "Analysis of your electricity consumption",
#         "com.grandlyon.grdf.read": "Analysis of your gas consumption",
#         "com.grandlyon.egl.read": "Analysis of your water consumption",
#     },
# )


# async def get_current_user(
#     security_scopes: SecurityScopes,
#     token: Annotated[str, Depends(oauth2_scheme)],
#     authenticator: Annotated[AbstractAuthenticator, Depends(authenticator)],
# ) -> Client:
#     credentials_exception = HTTPException(status_code=401, detail="Invalid credentials")
#     try:
#         payload = authenticator.decode_token(token)
#         scopes = payload.get("scope", "").split(" ")
#         for scope in security_scopes.scopes:
#             if scope not in scopes:
#                 raise HTTPException(status_code=403, detail="Not enough permissions")
#         client = authenticator.authenticate(token)
#         if client is None:
#             raise credentials_exception
#         return client
#     except (JWTError, ValidationError):
#         raise credentials_exception


# async def get_current_active_user(
#     client: Annotated[Client, Security(get_current_user)]
# ) -> Client:
#     if not client.access_token:
#         raise HTTPException(status_code=400, detail="Inactive client")
#     return client
