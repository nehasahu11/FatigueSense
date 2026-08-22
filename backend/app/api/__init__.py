from backend.app.api.routes.analyze import router as analyze_router
from backend.app.api.routes.upload import router as upload_router
from backend.app.api.routes.history import router as history_router
from backend.app.api.routes.documents import router as documents_router
from backend.app.api.routes.health import router as health_router


all_routers = [

    analyze_router,

    upload_router,

    history_router,

    documents_router,

    health_router
]
