from typing import Optional

from pydantic import BaseModel, Field


class FaceBoundingBox(BaseModel):
    """
    Bounding box information for a detected face.
    """

    x: int
    y: int
    width: int
    height: int

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )


class CVFeatureSchema(BaseModel):
    """
    Structured computer-vision features extracted
    from a facial image.

    This schema is the contract between:

        FeatureExtractor
              ↓
        ImageAnalysisAgent
              ↓
        FatigueScoringAgent
    """

    # ---------------------------------------------------------
    # Face detection
    # ---------------------------------------------------------

    face_detected: bool

    face_count: int = Field(
        ge=0
    )

    faces: list[FaceBoundingBox] = Field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Eye features
    # ---------------------------------------------------------

    left_ear: Optional[float] = Field(
        default=None,
        ge=0.0
    )

    right_ear: Optional[float] = Field(
        default=None,
        ge=0.0
    )

    average_ear: Optional[float] = Field(
        default=None,
        ge=0.0
    )

    eye_state: str = "unknown"

    # ---------------------------------------------------------
    # Blink / eye closure features
    # ---------------------------------------------------------

    left_eye_closed: bool = False

    right_eye_closed: bool = False

    both_eyes_closed: bool = False

    possible_blink: bool = False

    # ---------------------------------------------------------
    # Mouth / yawn features
    # ---------------------------------------------------------

    mouth_aspect_ratio: Optional[float] = Field(
        default=None,
        ge=0.0
    )

    yawn_detected: bool = False

    # ---------------------------------------------------------
    # Under-eye / dark-circle features
    # ---------------------------------------------------------

    left_under_eye_darkness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    right_under_eye_darkness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    average_under_eye_darkness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0
    )

    dark_circle_present: bool = False