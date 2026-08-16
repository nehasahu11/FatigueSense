from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class AnalysisState:
    user_id: str

    image_name: Optional[str] = None
    image_path: Optional[str] = None

    # Output from ImageAnalysisAgent
    features: Dict[str, Any] = field(default_factory=dict)

    # Output from RAG
    rag_context: List[str] = field(default_factory=list)

    # Output from FatigueScoringAgent
    fatigue_score: Optional[float] = None
    risk_level: Optional[str] = None

    # Output from RecommendationAgent
    recommendation: Optional[str] = None

    # Error information
    error: Optional[str] = None