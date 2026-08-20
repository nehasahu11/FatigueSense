from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from app.api.dependencies import (
    get_analysis_service
)

from app.services.analysis_service import (
    AnalysisService
)


router = APIRouter(
    prefix="/api",
    tags=["Analysis"]
)


@router.post("/analyze")
async def analyze_image(

    image_path: str,

    user_id: str = None,

    image_filename: str = "",

    service: AnalysisService = Depends(
        get_analysis_service
    )
):

    try:

        result = service.analyze(

            image_path=image_path,

            image_filename=image_filename,

            user_id=user_id
        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)
        )