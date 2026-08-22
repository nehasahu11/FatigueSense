from typing import Any, Dict, List, Optional
from typing_extensions import TypedDict


class FatigueState(TypedDict, total=False):
    """
    Shared state passed between LangGraph nodes.
    """

    session_id: str
    user_id: Optional[str]

    image_path: str
    image_filename: str

    # Member A
    cv_features: Dict[str, Any]
    fatigue_analysis: Dict[str, Any]
    fatigue_score: float
    risk_level: str

    # Member B
    rag_context: List[Any]
    evidence: List[str]
    rag_recommendation: str

    # Memory
    previous_sessions: List[Dict[str, Any]]

    # Final output
    recommendation: str
    final_response: Dict[str, Any]

    # Error
    error: Optional[str]