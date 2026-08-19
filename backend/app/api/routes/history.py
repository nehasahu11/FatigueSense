from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.api.dependencies import (
    get_history_service
)

from app.services.history_service import (
    HistoryService
)


router = APIRouter(
    prefix="/api",
    tags=["History"]
)


@router.get("/history/{user_id}")
async def history(

    user_id: str,

    limit: int = 20,

    service: HistoryService = Depends(
        get_history_service
    )
):

    try:

        return service.get_history(
            user_id,
            limit
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.get("/history/session/{session_id}")
async def get_session(

    session_id: str,

    service: HistoryService = Depends(
        get_history_service
    )
):

    result = service.get_analysis(
        session_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    return result