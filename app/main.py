import os
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.api.controllers.clients import router as clients
from app.api.controllers.documents import router as documents

app = FastAPI(
    title="Ecolyo Home Monitor",
)

# --------------------------------------------------------------------------------
# Security
# --------------------------------------------------------------------------------
app.swagger_ui_init_oauth = {
    "usePkceWithAuthorizationCodeGrant": True,
    "clientId": "cozy-swagger",
    "clientSecret": "vEAl7phmo1WHXBrdSsXoHSsk0lNMPIlX",
}


# --------------------------------------------------------------------------------
# Middlewares
# --------------------------------------------------------------------------------
@app.middleware("http")
async def cors_middlewares(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response


app.add_middleware(SessionMiddleware, secret_key=os.environ.get("APP_SECRET"))

# --------------------------------------------------------------------------------
# Routers
# --------------------------------------------------------------------------------
app.include_router(clients)
app.include_router(documents)
