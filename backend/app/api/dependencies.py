from app.services.analysis_service import (
    AnalysisService
)

from app.services.upload_service import (
    UploadService
)

from app.services.history_service import (
    HistoryService
)


analysis_service = AnalysisService()

upload_service = UploadService()

history_service = HistoryService()


def get_analysis_service():

    return analysis_service


def get_upload_service():

    return upload_service


def get_history_service():

    return history_service