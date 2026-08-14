import cv2
import numpy as np


class FacialFeatureAnalyzer:
    """
    Extract additional facial features related to fatigue.

    Currently analyzes:
        - Under-eye darkness
        - Approximate dark-circle presence

    This is an image-based heuristic and should not be
    interpreted as a medical diagnosis.
    """

    # ---------------------------------------------------------
    # Initial threshold.
    #
    # This will be calibrated later using the project's
    # test images.
    # ---------------------------------------------------------

    DARK_CIRCLE_THRESHOLD = 0.35

    # MediaPipe face landmark indices for approximate
    # under-eye regions.
    #
    # Left eye region
    LEFT_EYE_TOP = 159
    LEFT_EYE_BOTTOM = 145
    LEFT_EYE_OUTER = 33
    LEFT_EYE_INNER = 133

    # Right eye region
    RIGHT_EYE_TOP = 386
    RIGHT_EYE_BOTTOM = 374
    RIGHT_EYE_OUTER = 362
    RIGHT_EYE_INNER = 263

    def __init__(self):
        """
        Initialize the facial feature analyzer.
        """
        pass

    @staticmethod
    def _landmark_to_pixel(
        landmark,
        image_width: int,
        image_height: int
    ) -> tuple[int, int]:
        """
        Convert a normalized MediaPipe landmark into
        pixel coordinates.
        """

        x = int(
            landmark.x * image_width
        )

        y = int(
            landmark.y * image_height
        )

        x = max(
            0,
            min(image_width - 1, x)
        )

        y = max(
            0,
            min(image_height - 1, y)
        )

        return x, y

    @staticmethod
    def _get_region_mean(
        gray_image: np.ndarray,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> float:
        """
        Calculate average grayscale intensity
        inside a rectangular region.
        """

        height, width = gray_image.shape[:2]

        x1 = max(0, min(width - 1, x1))
        x2 = max(0, min(width - 1, x2))

        y1 = max(0, min(height - 1, y1))
        y2 = max(0, min(height - 1, y2))

        if x2 <= x1 or y2 <= y1:
            return 0.0

        region = gray_image[y1:y2, x1:x2]

        if region.size == 0:
            return 0.0

        return float(np.mean(region))

    def calculate_under_eye_darkness(
        self,
        image: np.ndarray,
        landmarks
    ) -> dict:
        """
        Estimate darkness below each eye.

        The score is based on the relative difference between
        the under-eye region and a nearby reference facial region.

        Returns:
            left_darkness
            right_darkness
            average_darkness
            dark_circle_present
        """

        if image is None:
            raise ValueError("Image cannot be None.")

        if not isinstance(image, np.ndarray):
            raise TypeError(
                "Image must be a NumPy array."
            )

        if image.size == 0:
            raise ValueError(
                "Image cannot be empty."
            )

        height, width = image.shape[:2]

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        # -----------------------------------------------------
        # Convert eye landmarks to pixels
        # -----------------------------------------------------

        left_top = self._landmark_to_pixel(
            landmarks[self.LEFT_EYE_TOP],
            width,
            height
        )

        left_bottom = self._landmark_to_pixel(
            landmarks[self.LEFT_EYE_BOTTOM],
            width,
            height
        )

        left_outer = self._landmark_to_pixel(
            landmarks[self.LEFT_EYE_OUTER],
            width,
            height
        )

        left_inner = self._landmark_to_pixel(
            landmarks[self.LEFT_EYE_INNER],
            width,
            height
        )

        right_top = self._landmark_to_pixel(
            landmarks[self.RIGHT_EYE_TOP],
            width,
            height
        )

        right_bottom = self._landmark_to_pixel(
            landmarks[self.RIGHT_EYE_BOTTOM],
            width,
            height
        )

        right_outer = self._landmark_to_pixel(
            landmarks[self.RIGHT_EYE_OUTER],
            width,
            height
        )

        right_inner = self._landmark_to_pixel(
            landmarks[self.RIGHT_EYE_INNER],
            width,
            height
        )

        # -----------------------------------------------------
        # Determine approximate eye widths
        # -----------------------------------------------------

        left_eye_width = abs(
            left_inner[0] - left_outer[0]
        )

        right_eye_width = abs(
            right_inner[0] - right_outer[0]
        )

        # -----------------------------------------------------
        # Under-eye region
        # -----------------------------------------------------

        left_x1 = min(
            left_outer[0],
            left_inner[0]
        )

        left_x2 = max(
            left_outer[0],
            left_inner[0]
        )

        left_y = max(
            left_top[1],
            left_bottom[1]
        )

        left_y1 = left_y
        left_y2 = left_y + max(
            3,
            int(left_eye_width * 0.35)
        )

        right_x1 = min(
            right_outer[0],
            right_inner[0]
        )

        right_x2 = max(
            right_outer[0],
            right_inner[0]
        )

        right_y = max(
            right_top[1],
            right_bottom[1]
        )

        right_y1 = right_y
        right_y2 = right_y + max(
            3,
            int(right_eye_width * 0.35)
        )

        # -----------------------------------------------------
        # Reference regions slightly below the under-eye
        # region.
        # -----------------------------------------------------

        left_reference_y1 = left_y2
        left_reference_y2 = left_y2 + max(
            5,
            int(left_eye_width * 0.5)
        )

        right_reference_y1 = right_y2
        right_reference_y2 = right_y2 + max(
            5,
            int(right_eye_width * 0.5)
        )

        # -----------------------------------------------------
        # Calculate grayscale means
        # -----------------------------------------------------

        left_under_eye = self._get_region_mean(
            gray,
            left_x1,
            left_y1,
            left_x2,
            left_y2
        )

        left_reference = self._get_region_mean(
            gray,
            left_x1,
            left_reference_y1,
            left_x2,
            left_reference_y2
        )

        right_under_eye = self._get_region_mean(
            gray,
            right_x1,
            right_y1,
            right_x2,
            right_y2
        )

        right_reference = self._get_region_mean(
            gray,
            right_x1,
            right_reference_y1,
            right_x2,
            right_reference_y2
        )

        # -----------------------------------------------------
        # Relative darkness
        #
        # Positive value = under-eye region is darker
        # than its nearby reference region.
        # -----------------------------------------------------

        left_difference = max(
            0.0,
            left_reference - left_under_eye
        )

        right_difference = max(
            0.0,
            right_reference - right_under_eye
        )

        # Normalize approximately to 0–1.
        left_darkness = min(
            1.0,
            left_difference / 80.0
        )

        right_darkness = min(
            1.0,
            right_difference / 80.0
        )

        average_darkness = (
            left_darkness + right_darkness
        ) / 2.0

        dark_circle_present = (
            average_darkness
            >= self.DARK_CIRCLE_THRESHOLD
        )

        return {
            "left_under_eye_darkness": float(
                left_darkness
            ),
            "right_under_eye_darkness": float(
                right_darkness
            ),
            "average_under_eye_darkness": float(
                average_darkness
            ),
            "dark_circle_present": bool(
                dark_circle_present
            )
        }

    def analyze(
        self,
        image: np.ndarray,
        landmarks
    ) -> dict:
        """
        Analyze additional facial features.

        Args:
            image: OpenCV BGR image.
            landmarks: MediaPipe facial landmarks.

        Returns:
            Facial feature dictionary.
        """

        if landmarks is None:
            return {
                "left_under_eye_darkness": None,
                "right_under_eye_darkness": None,
                "average_under_eye_darkness": None,
                "dark_circle_present": False
            }

        return self.calculate_under_eye_darkness(
            image,
            landmarks
        )