from fastapi import APIRouter


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


@router.get("/")
async def list_documents():

    return {
        "status": "success",
        "documents": []
    }


@router.get("/health")
async def document_health():

    return {
        "status": "ready",
        "message": "RAG document service available"
    }