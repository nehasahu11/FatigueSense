from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


class EyeAnalyzer:
    """
    Extract eye landmarks and calculate Eye Aspect Ratio (EAR).
    """

    # ---------------------------------------------------------
    # Initial EAR thresholds
    # These can be calibrated later using the team's
    # rested / mild-fatigue / high-fatigue test images.
    # ---------------------------------------------------------

    EYE_CLOSED_THRESHOLD = 0.20
    EYE_PARTIALLY_CLOSED_THRESHOLD = 0.25

    # ---------------------------------------------------------
    # MediaPipe Face Landmarker eye landmark indices
    # ---------------------------------------------------------

    # Left eye
    LEFT_EYE = [
        33,    # left corner
        160,   # upper
        158,   # upper
        133,   # right corner
        153,   # lower
        144    # lower
    ]

    # Right eye
    RIGHT_EYE = [
        362,   # left corner
        385,   # upper
        387,   # upper
        263,   # right corner
        373,   # lower
        380    # lower
    ]

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

        # -----------------------------------------------------
        # MediaPipe Base Options
        # -----------------------------------------------------

        base_options = mp.tasks.BaseOptions(
            model_asset_path=str(self.model_path)
        )

        # -----------------------------------------------------
        # Face Landmarker Options
        # -----------------------------------------------------

        options = mp.tasks.vision.FaceLandmarkerOptions(
            base_options=base_options,
            running_mode=mp.tasks.vision.RunningMode.IMAGE,
            num_faces=1
        )

        # -----------------------------------------------------
        # Create Face Landmarker
        # -----------------------------------------------------

        self.landmarker = (
            mp.tasks.vision.FaceLandmarker.create_from_options(
                options
            )
        )

    def get_landmarks(
        self,
        image: np.ndarray
    ):
        """
        Detect facial landmarks.

        Args:
            image: OpenCV BGR image.

        Returns:
            Facial landmarks for the first detected face,
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

        # -----------------------------------------------------
        # OpenCV BGR → RGB
        # MediaPipe expects RGB.
        # -----------------------------------------------------

        rgb_image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        # -----------------------------------------------------
        # Convert NumPy array → MediaPipe Image
        # -----------------------------------------------------

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # -----------------------------------------------------
        # Run face landmark detection
        # -----------------------------------------------------

        result = self.landmarker.detect(mp_image)

        if not result.face_landmarks:
            return None

        # Return landmarks for the first face
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

    def calculate_ear(self, landmarks) -> dict:
        """
        Calculate Eye Aspect Ratio (EAR) for both eyes.

        EAR formula:

            EAR = (vertical_distance_1 + vertical_distance_2)
                  / (2 * horizontal_distance)

        Returns:
            Dictionary containing:
                left_ear
                right_ear
                average_ear
        """

        # -----------------------------------------------------
        # Extract required landmarks
        # -----------------------------------------------------

        left = [
            landmarks[index]
            for index in self.LEFT_EYE
        ]

        right = [
            landmarks[index]
            for index in self.RIGHT_EYE
        ]

        # -----------------------------------------------------
        # LEFT EYE EAR
        # -----------------------------------------------------

        left_vertical_1 = self._distance(
            left[1],
            left[5]
        )

        left_vertical_2 = self._distance(
            left[2],
            left[4]
        )

        left_horizontal = self._distance(
            left[0],
            left[3]
        )

        if left_horizontal == 0:
            raise ValueError(
                "Invalid left eye landmarks: "
                "horizontal distance is zero."
            )

        left_ear = (
            left_vertical_1 + left_vertical_2
        ) / (2.0 * left_horizontal)

        # -----------------------------------------------------
        # RIGHT EYE EAR
        # -----------------------------------------------------

        right_vertical_1 = self._distance(
            right[1],
            right[5]
        )

        right_vertical_2 = self._distance(
            right[2],
            right[4]
        )

        right_horizontal = self._distance(
            right[0],
            right[3]
        )

        if right_horizontal == 0:
            raise ValueError(
                "Invalid right eye landmarks: "
                "horizontal distance is zero."
            )

        right_ear = (
            right_vertical_1 + right_vertical_2
        ) / (2.0 * right_horizontal)

        # -----------------------------------------------------
        # Average EAR
        # -----------------------------------------------------

        average_ear = (
            left_ear + right_ear
        ) / 2.0

        return {
            "left_ear": float(left_ear),
            "right_ear": float(right_ear),
            "average_ear": float(average_ear)
        }

    @classmethod
    def classify_eye_state(cls, ear: float) -> str:
        """
        Classify eye state based on average EAR.

        Args:
            ear: Average Eye Aspect Ratio.

        Returns:
            One of:
                "closed"
                "partially_closed"
                "open"
        """

        if ear < cls.EYE_CLOSED_THRESHOLD:
            return "closed"

        if ear < cls.EYE_PARTIALLY_CLOSED_THRESHOLD:
            return "partially_closed"

        return "open"

    def analyze(self, image: np.ndarray) -> dict:
        """
        Detect facial landmarks and calculate eye features.

        Returns:
            Dictionary containing face detection status,
            EAR values, and eye state.
        """

        landmarks = self.get_landmarks(image)

        # -----------------------------------------------------
        # No face detected
        # -----------------------------------------------------

        if landmarks is None:
            return {
                "face_detected": False,
                "left_ear": None,
                "right_ear": None,
                "average_ear": None,
                "eye_state": "unknown"
            }

        # -----------------------------------------------------
        # Calculate EAR
        # -----------------------------------------------------

        ear = self.calculate_ear(landmarks)

        # -----------------------------------------------------
        # Classify eye state
        # -----------------------------------------------------

        eye_state = self.classify_eye_state(
            ear["average_ear"]
        )

        return {
            "face_detected": True,
            "left_ear": ear["left_ear"],
            "right_ear": ear["right_ear"],
            "average_ear": ear["average_ear"],
            "eye_state": eye_state
        }

    def close(self):
        """
        Release MediaPipe resources.
        """

        self.landmarker.close()