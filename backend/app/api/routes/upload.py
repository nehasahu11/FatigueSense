from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Depends
)

from app.api.dependencies import (
    get_upload_service
)

from app.services.upload_service import (
    UploadService
)


router = APIRouter(
    prefix="/api",
    tags=["Upload"]
)


@router.post("/upload")
async def upload_image(

    image: UploadFile = File(...),

    service: UploadService = Depends(
        get_upload_service
    )
):

    try:

        path = service.save_file(
            image
        )

        return {

            "status": "success",

            "filename":
                image.filename,

            "path":
                path
        }

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