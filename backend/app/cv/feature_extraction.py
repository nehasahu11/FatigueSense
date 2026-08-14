from pathlib import Path

import numpy as np

from .face_detection import FaceDetector
from .eye_analysis import EyeAnalyzer
from .yawn_detection import YawnDetector
from .facial_features import FacialFeatureAnalyzer
from .blink_detection import BlinkDetector


class FeatureExtractor:
    """
    Combines all computer vision modules into one
    fatigue-feature extraction pipeline.

    Pipeline:

        Image
          ↓
        Face Detection
          ↓
        Facial Landmarks
          ↓
        ┌────────────────┬────────────────┬────────────────────┐
        ↓                ↓                ↓
    Eye Analysis    Yawn Detection   Facial Features
        ↓                ↓                ↓
        └────────────────┴────────────────┘
                         ↓
                  Blink Detection
                         ↓
               Structured CV Features
    """

    def __init__(self, model_directory: str):
        """
        Initialize all CV detectors.

        Args:
            model_directory:
                Directory containing the MediaPipe models.
        """

        self.model_directory = Path(model_directory)

        if not self.model_directory.exists():
            raise FileNotFoundError(
                f"Model directory not found: "
                f"{self.model_directory}"
            )

        # -----------------------------------------------------
        # Model paths
        # -----------------------------------------------------

        face_model = (
            self.model_directory
            / "blaze_face_short_range.tflite"
        )

        landmark_model = (
            self.model_directory
            / "face_landmarker.task"
        )

        # -----------------------------------------------------
        # Initialize CV components
        # -----------------------------------------------------

        self.face_detector = FaceDetector(
            str(face_model)
        )

        self.eye_analyzer = EyeAnalyzer(
            str(landmark_model)
        )

        self.yawn_detector = YawnDetector(
            str(landmark_model)
        )

        self.facial_feature_analyzer = (
            FacialFeatureAnalyzer()
        )

        self.blink_detector = BlinkDetector()

    def extract(self, image: np.ndarray) -> dict:
        """
        Extract all fatigue-related CV features.

        Args:
            image:
                Preprocessed OpenCV BGR image.

        Returns:
            Structured dictionary containing:

                Face:
                - face_detected
                - face_count
                - faces

                Eyes:
                - left_ear
                - right_ear
                - average_ear
                - eye_state

                Blink / eye closure:
                - left_eye_closed
                - right_eye_closed
                - both_eyes_closed
                - possible_blink

                Yawn:
                - mouth_aspect_ratio
                - yawn_detected

                Facial features:
                - left_under_eye_darkness
                - right_under_eye_darkness
                - average_under_eye_darkness
                - dark_circle_present
        """

        # -----------------------------------------------------
        # Validate image
        # -----------------------------------------------------

        if image is None:
            raise ValueError(
                "Image cannot be None."
            )

        if not isinstance(image, np.ndarray):
            raise TypeError(
                "Image must be a NumPy array."
            )

        if image.size == 0:
            raise ValueError(
                "Image cannot be empty."
            )

        # =====================================================
        # 1. FACE DETECTION
        # =====================================================

        faces = self.face_detector.detect(image)

        face_detected = len(faces) > 0

        # -----------------------------------------------------
        # No face found
        # -----------------------------------------------------

        if not face_detected:
            return {
                # Face
                "face_detected": False,
                "face_count": 0,
                "faces": [],

                # Eyes
                "left_ear": None,
                "right_ear": None,
                "average_ear": None,
                "eye_state": "unknown",

                # Blink / eye closure
                "left_eye_closed": False,
                "right_eye_closed": False,
                "both_eyes_closed": False,
                "possible_blink": False,

                # Yawn
                "mouth_aspect_ratio": None,
                "yawn_detected": False,

                # Facial features
                "left_under_eye_darkness": None,
                "right_under_eye_darkness": None,
                "average_under_eye_darkness": None,
                "dark_circle_present": False
            }

        # =====================================================
        # 2. GET FACIAL LANDMARKS
        # =====================================================

        landmarks = self.eye_analyzer.get_landmarks(
            image
        )

        # -----------------------------------------------------
        # Safety check
        # -----------------------------------------------------

        if landmarks is None:
            return {
                # Face
                "face_detected": True,
                "face_count": len(faces),
                "faces": faces,

                # Eyes
                "left_ear": None,
                "right_ear": None,
                "average_ear": None,
                "eye_state": "unknown",

                # Blink / eye closure
                "left_eye_closed": False,
                "right_eye_closed": False,
                "both_eyes_closed": False,
                "possible_blink": False,

                # Yawn
                "mouth_aspect_ratio": None,
                "yawn_detected": False,

                # Facial features
                "left_under_eye_darkness": None,
                "right_under_eye_darkness": None,
                "average_under_eye_darkness": None,
                "dark_circle_present": False
            }

        # =====================================================
        # 3. EYE ANALYSIS
        # =====================================================

        eye_features = (
            self.eye_analyzer.calculate_ear(
                landmarks
            )
        )

        eye_state = (
            self.eye_analyzer.classify_eye_state(
                eye_features["average_ear"]
            )
        )

        # =====================================================
        # 4. BLINK / EYE CLOSURE ANALYSIS
        # =====================================================

        blink_features = (
            self.blink_detector.analyze(
                eye_features["left_ear"],
                eye_features["right_ear"]
            )
        )

        # =====================================================
        # 5. YAWN ANALYSIS
        # =====================================================

        mouth_aspect_ratio = (
            self.yawn_detector.calculate_mar(
                landmarks
            )
        )

        yawn_detected = (
            self.yawn_detector.classify_yawn(
                mouth_aspect_ratio
            )
        )

        # =====================================================
        # 6. FACIAL FEATURE ANALYSIS
        # =====================================================

        facial_features = (
            self.facial_feature_analyzer.analyze(
                image,
                landmarks
            )
        )

        # =====================================================
        # 7. COMBINE ALL FEATURES
        # =====================================================

        return {
            # -------------------------------------------------
            # Face
            # -------------------------------------------------

            "face_detected": True,

            "face_count": len(faces),

            "faces": faces,

            # -------------------------------------------------
            # Eyes
            # -------------------------------------------------

            "left_ear": (
                eye_features["left_ear"]
            ),

            "right_ear": (
                eye_features["right_ear"]
            ),

            "average_ear": (
                eye_features["average_ear"]
            ),

            "eye_state": eye_state,

            # -------------------------------------------------
            # Blink / Eye Closure
            # -------------------------------------------------

            "left_eye_closed": (
                blink_features["left_eye_closed"]
            ),

            "right_eye_closed": (
                blink_features["right_eye_closed"]
            ),

            "both_eyes_closed": (
                blink_features["both_eyes_closed"]
            ),

            "possible_blink": (
                blink_features["possible_blink"]
            ),

            # -------------------------------------------------
            # Mouth / Yawn
            # -------------------------------------------------

            "mouth_aspect_ratio": (
                mouth_aspect_ratio
            ),

            "yawn_detected": (
                yawn_detected
            ),

            # -------------------------------------------------
            # Under-eye / Dark circles
            # -------------------------------------------------

            "left_under_eye_darkness": (
                facial_features[
                    "left_under_eye_darkness"
                ]
            ),

            "right_under_eye_darkness": (
                facial_features[
                    "right_under_eye_darkness"
                ]
            ),

            "average_under_eye_darkness": (
                facial_features[
                    "average_under_eye_darkness"
                ]
            ),

            "dark_circle_present": (
                facial_features[
                    "dark_circle_present"
                ]
            )
        }

    def close(self):
        """
        Release resources used by all CV modules.
        """

        self.face_detector.close()

        self.eye_analyzer.close()

        self.yawn_detector.close()