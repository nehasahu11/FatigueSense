from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class FatigueState(TypedDict, total=False):
    session_id: str
    user_id: Optional[str]

    image_path: str
    image_filename: str

    # Member A output
    cv_features: Dict[str, Any]
    fatigue_score: float
    risk_level: str
    fatigue_analysis: Dict[str, Any]

    # Member B output
    rag_context: List[Dict[str, Any]]
    evidence: List[str]
    rag_recommendation: str

    # Final result
    recommendation: str
    final_response: Dict[str, Any]

    # Memory
    previous_sessions: List[Dict[str, Any]]

    # Error handling
    error: Optional[str]