from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AnalysisResponse(BaseModel):

    session_id: str

    fatigue_score: float = Field(
        ge=0,
        le=100
    )

    risk_level: str

    cv_features: Dict[str, Any] = {}

    analysis: Dict[str, Any] = {}

    recommendation: str

    evidence: List[str] = []

    status: str

    error: Optional[str] = None