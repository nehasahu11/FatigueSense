from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from app.api.dependencies import (
    get_analysis_service,
    get_upload_service
)

from app.services.analysis_service import (
    AnalysisService
)

from app.services.upload_service import (
    UploadService
)


router = APIRouter(
    prefix="/api",
    tags=["Analysis"]
)


@router.post("/analyze")
async def analyze_image(
    images: UploadFile = File(...),

    user_id: str = Form(...),

    service: AnalysisService = Depends(
        get_analysis_service
    ),

    upload_service: UploadService = Depends(
        get_upload_service
    )
):

    try:

        # -----------------------------------------
        # Save uploaded image
        # -----------------------------------------

        image_path = upload_service.save_file(
            images
        )

        # -----------------------------------------
        # Run LangGraph workflow
        # -----------------------------------------

        result = service.analyze(

            image_path=image_path,

            image_filename=images.filename or "",

            user_id=user_id
        )

        # -----------------------------------------
        # Return analysis result
        # -----------------------------------------

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
