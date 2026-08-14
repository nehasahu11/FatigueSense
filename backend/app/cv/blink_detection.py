class BlinkDetector:
    """
    Estimate possible eye closure using Eye Aspect Ratio (EAR).

    Note:
        True blink detection requires temporal information
        from multiple video frames. For single-image analysis,
        this class identifies possible eye closure based on EAR.
    """

    # EAR below this value is considered possible eye closure.
    EAR_CLOSURE_THRESHOLD = 0.21

    def __init__(self, threshold: float = EAR_CLOSURE_THRESHOLD):
        """
        Initialize the blink detector.

        Args:
            threshold:
                EAR threshold below which the eyes are considered
                possibly closed.
        """

        if threshold <= 0:
            raise ValueError(
                "EAR threshold must be greater than 0."
            )

        self.threshold = float(threshold)

    def is_eye_closed(self, ear: float) -> bool:
        """
        Determine whether an eye appears closed based on EAR.

        Args:
            ear:
                Eye Aspect Ratio.

        Returns:
            True if the EAR indicates possible eye closure.
        """

        if ear is None:
            return False

        if ear < 0:
            raise ValueError(
                "EAR cannot be negative."
            )

        return ear < self.threshold

    def analyze(
        self,
        left_ear: float | None,
        right_ear: float | None
    ) -> dict:
        """
        Analyze both eyes using their EAR values.

        Args:
            left_ear:
                EAR value for the left eye.

            right_ear:
                EAR value for the right eye.

        Returns:
            Dictionary containing eye closure information.
        """

        if left_ear is None or right_ear is None:
            return {
                "left_eye_closed": False,
                "right_eye_closed": False,
                "both_eyes_closed": False,
                "possible_blink": False
            }

        left_closed = self.is_eye_closed(left_ear)
        right_closed = self.is_eye_closed(right_ear)

        both_closed = (
            left_closed and right_closed
        )

        return {
            "left_eye_closed": left_closed,
            "right_eye_closed": right_closed,
            "both_eyes_closed": both_closed,
            "possible_blink": both_closed
        }