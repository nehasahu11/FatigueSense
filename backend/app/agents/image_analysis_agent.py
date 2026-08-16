from pathlib import Path

from ..cv.feature_extraction import FeatureExtractor
from ..schemas.cv_feature_schema import CVFeatureSchema
from ..preprocessing.image_preprocessor import preprocess_image


class ImageAnalysisAgent:
    """
    AI agent responsible for analyzing an uploaded image.

    Responsibilities:
        1. Validate/preprocess image
        2. Extract computer-vision features
        3. Validate extracted features
        4. Return structured CV analysis

    The agent does NOT calculate the final fatigue score.

    Fatigue scoring is handled separately by:
        FatigueScoringAgent
    """

    def __init__(self, model_directory: str):
        """
        Initialize the Image Analysis Agent.

        Args:
            model_directory:
                Directory containing MediaPipe models.
        """

        self.model_directory = Path(model_directory)

        if not self.model_directory.exists():
            raise FileNotFoundError(
                f"Model directory not found: {self.model_directory}"
            )

        self.feature_extractor = FeatureExtractor(
            str(self.model_directory)
        )

    def analyze(self, image_path: str) -> dict:
        """
        Analyze an uploaded image.

        Args:
            image_path:
                Path to the uploaded image.

        Returns:
            Validated CV feature dictionary.
        """

        # ---------------------------------------------------------
        # 1. Validate image path
        # ---------------------------------------------------------

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        if not image_path.is_file():
            raise ValueError(
                f"Image path is not a file: {image_path}"
            )

        # ---------------------------------------------------------
        # 2. Preprocess image
        # ---------------------------------------------------------

        image = preprocess_image(
            str(image_path)
        )

        # ---------------------------------------------------------
        # 3. Extract CV features
        # ---------------------------------------------------------

        features = self.feature_extractor.extract(
            image
        )

        # ---------------------------------------------------------
        # 4. Validate using Pydantic schema
        # ---------------------------------------------------------

        validated_features = CVFeatureSchema.model_validate(
            features
        )

        # ---------------------------------------------------------
        # 5. Return validated structured result
        # ---------------------------------------------------------

        return validated_features.model_dump()

    def close(self):
        """
        Release resources used by the CV pipeline.
        """

        self.feature_extractor.close()