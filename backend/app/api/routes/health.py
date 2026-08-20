from fastapi import APIRouter


router = APIRouter(
    prefix="/api",
    tags=["Health"]
)


@router.get("/health")
async def health():

    return {

        "status": "healthy",

        "service":
            "FatigueSense",

        "version":
            "1.0.0"
    }