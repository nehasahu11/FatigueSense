from typing import Literal

from pydantic import BaseModel, Field


class FatigueComponents(BaseModel):
    """
    Individual contributions to the fatigue score.
    """

    eye_closure_score: float = Field(
        ge=0.0,
        le=40.0
    )

    eye_state_score: float = Field(
        ge=0.0,
        le=20.0
    )

    yawn_score: float = Field(
        ge=0.0,
        le=25.0
    )

    dark_circle_score: float = Field(
        ge=0.0,
        le=15.0
    )


class FatigueResult(BaseModel):
    """
    Final fatigue assessment produced by
    FatigueScoringAgent.
    """

    fatigue_score: float = Field(
        ge=0.0,
        le=100.0
    )

    risk_level: Literal[
        "Low",
        "Medium",
        "High"
    ]

    components: FatigueComponents