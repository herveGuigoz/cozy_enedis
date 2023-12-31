from fastapi import APIRouter, Depends, dependencies
from app.providers.dependencies import get_documents_usecase
from app.core.usecases.get_documents import (
    GetDocumentsCommand,
    GetDocumentsCommandHandler,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
    # dependencies=dependencies,
)


# --------------------------------------------------------------------------------
# Controllers
# --------------------------------------------------------------------------------
@router.get(
    "/{client_id}",
    response_model=dict,
    status_code=200,
)
async def get_documents(
    client_id: str,
    handler: GetDocumentsCommandHandler = Depends(get_documents_usecase),
) -> dict:
    command = GetDocumentsCommand(client_id=client_id)
    return handler(command)
