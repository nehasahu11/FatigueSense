from typing import Optional

from ..schemas.cv_feature_schema import CVFeatureSchema
from ..schemas.fatigue_schema import FatigueResult


class FatigueScoringAgent:
    """
    Converts computer-vision features into a fatigue score.

    Score:
        0   = lowest detected fatigue
        100 = highest detected fatigue

    Risk levels:
        Low
        Medium
        High

    This is a project-level heuristic and is NOT a
    medical diagnostic system.

    Scoring components:

        Eye closure / EAR       = 35
        Eye state               = 15
        Blink / eye closure     = 10
        Yawn                    = 25
        Under-eye darkness      = 15

        Total                   = 100
    """

    # ---------------------------------------------------------
    # EAR thresholds
    # ---------------------------------------------------------

    EAR_OPEN = 0.30
    EAR_CLOSED = 0.20

    # ---------------------------------------------------------
    # MAR thresholds
    # ---------------------------------------------------------

    MAR_NORMAL = 0.30
    MAR_YAWN = 0.60

    # ---------------------------------------------------------
    # Dark-circle threshold
    # ---------------------------------------------------------

    DARKNESS_THRESHOLD = 0.35

    # ---------------------------------------------------------
    # Risk thresholds
    # ---------------------------------------------------------

    LOW_RISK_MAX = 33
    MEDIUM_RISK_MAX = 66

    # ---------------------------------------------------------
    # Maximum scoring contributions
    # ---------------------------------------------------------

    MAX_EYE_SCORE = 35.0
    MAX_EYE_STATE_SCORE = 15.0
    MAX_BLINK_SCORE = 10.0
    MAX_YAWN_SCORE = 25.0
    MAX_DARK_CIRCLE_SCORE = 15.0

    # =========================================================
    # 1. EAR / EYE CLOSURE FATIGUE
    # =========================================================

    def calculate_eye_fatigue(
        self,
        average_ear: Optional[float]
    ) -> float:
        """
        Convert EAR into a 0-35 fatigue contribution.

        Lower EAR indicates greater eye closure.

        Scoring:
            EAR >= 0.30       -> 0
            EAR <= 0.20       -> 35
            Between           -> proportional score
        """

        if average_ear is None:
            return 0.0

        if average_ear < 0:
            raise ValueError(
                "EAR cannot be negative."
            )

        if average_ear >= self.EAR_OPEN:
            return 0.0

        if average_ear <= self.EAR_CLOSED:
            return self.MAX_EYE_SCORE

        ratio = (
            self.EAR_OPEN - average_ear
        ) / (
            self.EAR_OPEN - self.EAR_CLOSED
        )

        return float(
            max(
                0.0,
                min(
                    self.MAX_EYE_SCORE,
                    ratio * self.MAX_EYE_SCORE
                )
            )
        )

    # =========================================================
    # 2. EYE STATE
    # =========================================================

    def calculate_eye_state_fatigue(
        self,
        eye_state: str
    ) -> float:
        """
        Add a supporting score based on eye state.

        closed           -> 15
        partially_closed -> 7.5
        open             -> 0
        unknown          -> 0
        """

        if eye_state == "closed":
            return self.MAX_EYE_STATE_SCORE

        if eye_state == "partially_closed":
            return self.MAX_EYE_STATE_SCORE / 2.0

        return 0.0

    # =========================================================
    # 3. BLINK / EYE CLOSURE
    # =========================================================

    def calculate_blink_fatigue(
        self,
        left_eye_closed: bool,
        right_eye_closed: bool,
        both_eyes_closed: bool,
        possible_blink: bool
    ) -> float:
        """
        Calculate a supporting fatigue contribution from
        the blink / eye-closure detector.

        Important:
            Single-image analysis cannot measure actual blink
            frequency. Therefore this is treated as a possible
            eye-closure signal rather than true blink frequency.

        Scoring:

            Both eyes closed / possible blink -> 10
            One eye closed                   -> 5
            Eyes open                        -> 0
        """

        if both_eyes_closed or possible_blink:
            return self.MAX_BLINK_SCORE

        if left_eye_closed or right_eye_closed:
            return self.MAX_BLINK_SCORE / 2.0

        return 0.0

    # =========================================================
    # 4. YAWN FATIGUE
    # =========================================================

    def calculate_yawn_fatigue(
        self,
        mouth_aspect_ratio: Optional[float],
        yawn_detected: bool
    ) -> float:
        """
        Convert mouth opening/yawn information into
        a 0-25 fatigue contribution.

        Scoring:

            yawn detected       -> 25
            MAR <= 0.30         -> 0
            MAR >= 0.60         -> 20
            Between             -> proportional 0-20
        """

        if mouth_aspect_ratio is not None:

            if mouth_aspect_ratio < 0:
                raise ValueError(
                    "Mouth Aspect Ratio cannot be negative."
                )

        if yawn_detected:
            return self.MAX_YAWN_SCORE

        if mouth_aspect_ratio is None:
            return 0.0

        if mouth_aspect_ratio <= self.MAR_NORMAL:
            return 0.0

        if mouth_aspect_ratio >= self.MAR_YAWN:
            return 20.0

        ratio = (
            mouth_aspect_ratio - self.MAR_NORMAL
        ) / (
            self.MAR_YAWN - self.MAR_NORMAL
        )

        return float(
            max(
                0.0,
                min(
                    20.0,
                    ratio * 20.0
                )
            )
        )

    # =========================================================
    # 5. UNDER-EYE DARKNESS
    # =========================================================

    def calculate_dark_circle_fatigue(
        self,
        darkness: Optional[float],
        dark_circle_present: bool
    ) -> float:
        """
        Convert under-eye darkness into a
        0-15 fatigue contribution.

        Dark circles are treated as a weak supporting
        signal rather than a primary fatigue indicator.
        """

        if darkness is None:
            return 0.0

        if darkness < 0:
            raise ValueError(
                "Darkness cannot be negative."
            )

        darkness = min(
            1.0,
            darkness
        )

        if darkness <= self.DARKNESS_THRESHOLD:
            return 0.0

        ratio = (
            darkness - self.DARKNESS_THRESHOLD
        ) / (
            1.0 - self.DARKNESS_THRESHOLD
        )

        score = ratio * self.MAX_DARK_CIRCLE_SCORE

        # Add a small supporting contribution when the
        # detector explicitly identifies dark circles.
        if dark_circle_present:
            score += 2.0

        return float(
            max(
                0.0,
                min(
                    self.MAX_DARK_CIRCLE_SCORE,
                    score
                )
            )
        )

    # =========================================================
    # 6. FINAL SCORE
    # =========================================================

    def calculate_score(
        self,
        features: CVFeatureSchema
    ) -> dict:
        """
        Calculate the final fatigue score.

        The individual signals are combined into
        a normalized 0-100 score.
        """

        # -----------------------------------------------------
        # Eye / EAR
        # -----------------------------------------------------

        eye_score = self.calculate_eye_fatigue(
            features.average_ear
        )

        # -----------------------------------------------------
        # Eye state
        # -----------------------------------------------------

        eye_state_score = (
            self.calculate_eye_state_fatigue(
                features.eye_state
            )
        )

        # -----------------------------------------------------
        # Blink / eye closure
        # -----------------------------------------------------

        blink_score = (
            self.calculate_blink_fatigue(
                features.left_eye_closed,
                features.right_eye_closed,
                features.both_eyes_closed,
                features.possible_blink
            )
        )

        # -----------------------------------------------------
        # Yawn
        # -----------------------------------------------------

        yawn_score = self.calculate_yawn_fatigue(
            features.mouth_aspect_ratio,
            features.yawn_detected
        )

        # -----------------------------------------------------
        # Under-eye darkness
        # -----------------------------------------------------

        darkness_score = (
            self.calculate_dark_circle_fatigue(
                features.average_under_eye_darkness,
                features.dark_circle_present
            )
        )

        # -----------------------------------------------------
        # Combine scores
        # -----------------------------------------------------

        raw_score = (
            eye_score
            + eye_state_score
            + blink_score
            + yawn_score
            + darkness_score
        )

        # -----------------------------------------------------
        # Normalize to 0-100
        # -----------------------------------------------------

        final_score = max(
            0.0,
            min(
                100.0,
                raw_score
            )
        )

        # -----------------------------------------------------
        # Determine risk
        # -----------------------------------------------------

        risk_level = self.get_risk_level(
            final_score
        )

        # -----------------------------------------------------
        # Return result
        # -----------------------------------------------------

        return {
            "fatigue_score": round(
                final_score,
                2
            ),

            "risk_level": risk_level,

            "components": {
                "eye_closure_score": round(
                    eye_score,
                    2
                ),

                "eye_state_score": round(
                    eye_state_score,
                    2
                ),

                "blink_score": round(
                    blink_score,
                    2
                ),

                "yawn_score": round(
                    yawn_score,
                    2
                ),

                "dark_circle_score": round(
                    darkness_score,
                    2
                )
            }
        }

    # =========================================================
    # 7. RISK LEVEL
    # =========================================================

    def get_risk_level(
        self,
        score: float
    ) -> str:
        """
        Convert fatigue score into risk level.

        0-33   -> Low
        34-66  -> Medium
        67-100 -> High
        """

        if score < 0:
            raise ValueError(
                "Fatigue score cannot be negative."
            )

        if score <= self.LOW_RISK_MAX:
            return "Low"

        if score <= self.MEDIUM_RISK_MAX:
            return "Medium"

        return "High"

    # =========================================================
    # 8. PUBLIC METHOD
    # =========================================================

    def score(
        self,
        features: dict
    ) -> dict:
        """
        Public scoring method.

        Accepts a dictionary from ImageAnalysisAgent,
        validates it using CVFeatureSchema, calculates
        the fatigue score, and validates the final result
        using FatigueResult.
        """

        # -----------------------------------------------------
        # Validate incoming CV features
        # -----------------------------------------------------

        validated_features = (
            CVFeatureSchema.model_validate(
                features
            )
        )

        # -----------------------------------------------------
        # Calculate fatigue result
        # -----------------------------------------------------

        result = self.calculate_score(
            validated_features
        )

        # -----------------------------------------------------
        # Validate final fatigue result
        # -----------------------------------------------------

        validated_result = (
            FatigueResult.model_validate(
                result
            )
        )

        # -----------------------------------------------------
        # Return clean dictionary
        # -----------------------------------------------------

        return validated_result.model_dump()