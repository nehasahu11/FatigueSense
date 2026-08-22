from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


class YawnDetector:
    """
    Detect mouth opening and estimate possible yawning
    using MediaPipe Face Landmarker.
    """

    # ---------------------------------------------------------
    # Mouth landmark indices
    # ---------------------------------------------------------

    # Outer mouth landmarks
    MOUTH_LEFT = 61
    MOUTH_RIGHT = 291

    MOUTH_TOP = 13
    MOUTH_BOTTOM = 14

    # ---------------------------------------------------------
    # Initial mouth aspect ratio threshold.
    #
    # This is intentionally configurable and will be
    # calibrated using the project's test images.
    # ---------------------------------------------------------

    YAWN_THRESHOLD = 0.60

    def __init__(self, model_path: str):
        """
        Initialize MediaPipe Face Landmarker.

        Args:
            model_path: Path to face_landmarker.task.
        """

        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Face landmarker model not found: {self.model_path}"
            )

        base_options = mp.tasks.BaseOptions(
            model_asset_path=str(self.model_path)
        )

        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.IMAGE,
            num_faces=1
        )

        self.landmarker = (
            mp.tasks.vision.FaceLandmarker.create_from_options(
                options
            )
        )

    def get_landmarks(self, image: np.ndarray):
        """
        Detect facial landmarks.

        Args:
            image: OpenCV BGR image.

        Returns:
            Landmarks for the first detected face,
            or None if no face is detected.
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

        # OpenCV BGR → RGB
        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        # Convert to MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # Detect landmarks
        result = self.landmarker.detect(mp_image)

        if not result.face_landmarks:
            return None

        return result.face_landmarks[0]

    @staticmethod
    def _distance(point1, point2) -> float:
        """
        Calculate Euclidean distance between two landmarks.
        """

        return float(
            np.sqrt(
                (point1.x - point2.x) ** 2
                + (point1.y - point2.y) ** 2
            )
        )

    def calculate_mar(self, landmarks) -> float:
        """
        Calculate Mouth Aspect Ratio (MAR).

        MAR = vertical mouth opening / horizontal mouth width
        """

        mouth_left = landmarks[self.MOUTH_LEFT]
        mouth_right = landmarks[self.MOUTH_RIGHT]

        mouth_top = landmarks[self.MOUTH_TOP]
        mouth_bottom = landmarks[self.MOUTH_BOTTOM]

        vertical_distance = self._distance(
            mouth_top,
            mouth_bottom
        )

        horizontal_distance = self._distance(
            mouth_left,
            mouth_right
        )

        if horizontal_distance == 0:
            raise ValueError(
                "Invalid mouth landmarks: "
                "horizontal distance is zero."
            )

        mar = (
            vertical_distance
            / horizontal_distance
        )

        return float(mar)

    @classmethod
    def classify_yawn(cls, mar: float) -> bool:
        """
        Determine whether the mouth opening is large enough
        to be considered a possible yawn.

        Note:
            This is an image-level heuristic. True yawn
            detection is more reliable when temporal information
            from video frames is available.
        """

        return mar >= cls.YAWN_THRESHOLD

    def analyze(self, image: np.ndarray) -> dict:
        """
        Analyze mouth opening and possible yawn.
        """

        landmarks = self.get_landmarks(image)

        if landmarks is None:
            return {
                "face_detected": False,
                "mouth_aspect_ratio": None,
                "yawn_detected": False
            }

        mar = self.calculate_mar(landmarks)

        yawn_detected = self.classify_yawn(mar)

        return {
            "face_detected": True,
            "mouth_aspect_ratio": mar,
            "yawn_detected": yawn_detected
        }

    def close(self):
        """
        Release MediaPipe resources.
        """

        self.landmarker.close()