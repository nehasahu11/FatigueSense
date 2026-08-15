from backend.app.agents.image_analysis_agent import ImageAnalysisAgent
from backend.app.agents.fatigue_scoring_agent import FatigueScoringAgent


class CVFatigueService:
    """
    Public service interface for the Member-A
    computer-vision fatigue pipeline.

    Responsibilities:
        1. Analyze an input image.
        2. Extract validated CV features.
        3. Calculate the fatigue score.
        4. Return both CV features and fatigue result.

    Downstream modules should use this service
    instead of directly accessing internal CV modules.
    """

    def __init__(
        self,
        model_directory: str = "backend/data/models"
    ):
        self.image_agent = ImageAnalysisAgent(
            model_directory=model_directory
        )

        self.scoring_agent = FatigueScoringAgent()

    def analyze(
        self,
        image_path: str
    ) -> dict:
        """
        Run the complete Member-A pipeline.

        Returns:
            {
                "cv_features": {...},
                "fatigue_result": {...}
            }
        """

        # ---------------------------------------------
        # Step 1: Image → CV features
        # ---------------------------------------------

        cv_features = self.image_agent.analyze(
            image_path
        )

        # ---------------------------------------------
        # Step 2: CV features → fatigue result
        # ---------------------------------------------

        fatigue_result = self.scoring_agent.score(
            cv_features
        )

        # ---------------------------------------------
        # Step 3: Final structured output
        # ---------------------------------------------

        return {
            "cv_features": cv_features,
            "fatigue_result": fatigue_result
        }