from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np


class FaceDetector:
    """
    Face detector using the MediaPipe Tasks API.
    """

    def __init__(
        self,
        model_path: str,
        min_detection_confidence: float = 0.5
    ):
        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Face detection model not found: {self.model_path}"
            )

        base_options = mp.tasks.BaseOptions(
            model_asset_path=str(self.model_path)
        )

        options = mp.tasks.vision.FaceDetectorOptions(
            base_options=base_options,
            min_detection_confidence=min_detection_confidence
        )

        self.detector = (
            mp.tasks.vision.FaceDetector.create_from_options(
                options
            )
        )

    def detect(self, image: np.ndarray) -> list[dict]:
        """
        Detect faces in an OpenCV BGR image.

        Args:
            image: OpenCV BGR image.

        Returns:
            List of detected faces with bounding boxes
            and confidence scores.
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

        # Convert NumPy image to MediaPipe Image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_image
        )

        # Run face detection
        result = self.detector.detect(mp_image)

        faces = []

        height, width = image.shape[:2]

        for detection in result.detections:

            bounding_box = detection.bounding_box

            x = max(
                0,
                bounding_box.origin_x
            )

            y = max(
                0,
                bounding_box.origin_y
            )

            box_width = bounding_box.width
            box_height = bounding_box.height

            confidence = float(
                detection.categories[0].score
            )

            faces.append(
                {
                    "x": x,
                    "y": y,
                    "width": box_width,
                    "height": box_height,
                    "confidence": confidence
                }
            )

        return faces

    def close(self):
        """
        Release MediaPipe resources.
        """

        self.detector.close()