from pathlib import Path
from typing import Any, Dict


class AgentRouter:
    """
    Member D router.

    This class connects the LangGraph workflow
    with Member A and Member B components.
    """

    def __init__(self):

        self.image_agent = None
        self.fatigue_agent = None
        self.recommendation_agent = None
        self.rag_pipeline = None

        self._load_member_a()
        self._load_member_b()

    # =================================================
    # MEMBER A
    # =================================================

    def _load_member_a(self):
        """
        Load Member A agents.
        """

        # ---------------------------------------------
        # IMAGE ANALYSIS AGENT
        # ---------------------------------------------

        try:

            from app.agents.image_analysis_agent import (
                ImageAnalysisAgent
            )

            # router.py is located at:
            # backend/app/orchestration/router.py
            #
            # parents[2] gives:
            # backend/
            #
            # Therefore this points to:
            # backend/data/models/

            backend_dir = Path(__file__).resolve().parents[2]

            model_directory = (
                backend_dir / "data" / "models"
            )

            self.image_agent = ImageAnalysisAgent(
                model_directory=str(model_directory)
            )

            print(
                "ImageAnalysisAgent loaded successfully."
            )

        except Exception as e:

            print(
                f"Warning: ImageAnalysisAgent "
                f"could not be loaded: {e}"
            )

        # ---------------------------------------------
        # FATIGUE SCORING AGENT
        # ---------------------------------------------

        try:

            from app.agents.fatigue_scoring_agent import (
                FatigueScoringAgent
            )

            self.fatigue_agent = FatigueScoringAgent()

            print(
                "FatigueScoringAgent loaded successfully."
            )

        except Exception as e:

            print(
                f"Warning: FatigueScoringAgent "
                f"could not be loaded: {e}"
            )

        # ---------------------------------------------
        # RECOMMENDATION AGENT
        # ---------------------------------------------

        try:

            from app.agents.recommendation_agent import (
                RecommendationAgent
            )

            self.recommendation_agent = (
                RecommendationAgent()
            )

            print(
                "RecommendationAgent loaded successfully."
            )

        except Exception as e:

            print(
                f"Warning: RecommendationAgent "
                f"could not be loaded: {e}"
            )

    # =================================================
    # MEMBER B
    # =================================================

    def _load_member_b(self):
        """
        Load Member B RAG pipeline.
        """

        try:

            from app.rag.pipeline import RAGPipeline

            self.rag_pipeline = RAGPipeline()

            print(
                "RAGPipeline loaded successfully."
            )

        except Exception as e:

            print(
                f"Warning: RAGPipeline "
                f"could not be loaded: {e}"
            )

    # =================================================
    # IMAGE ANALYSIS
    # =================================================

    def run_image_analysis(
        self,
        image_path: str
    ) -> Dict[str, Any]:

        if self.image_agent is None:

            raise RuntimeError(
                "Member A ImageAnalysisAgent "
                "is not available."
            )

        # Some implementations use run()
        if hasattr(
            self.image_agent,
            "run"
        ):

            result = self.image_agent.run(
                image_path
            )

        # Your current ImageAnalysisAgent
        # actually uses analyze()
        elif hasattr(
            self.image_agent,
            "analyze"
        ):

            result = self.image_agent.analyze(
                image_path
            )

        else:

            raise AttributeError(
                "ImageAnalysisAgent must have "
                "run() or analyze()."
            )

        if isinstance(result, dict):

            return result

        return {
            "result": result
        }

    # =================================================
    # FATIGUE SCORE
    # =================================================

    def calculate_fatigue(
        self,
        cv_features: Dict[str, Any]
    ) -> Dict[str, Any]:

        if self.fatigue_agent is None:

            raise RuntimeError(
                "Member A FatigueScoringAgent "
                "is not available."
            )

        if hasattr(
            self.fatigue_agent,
            "run"
        ):

            result = self.fatigue_agent.run(
                cv_features
            )

        elif hasattr(
            self.fatigue_agent,
            "score"
        ):

            result = self.fatigue_agent.score(
                cv_features
            )

        else:

            raise AttributeError(
                "FatigueScoringAgent must have "
                "run() or score()."
            )

        if isinstance(result, dict):

            return result

        return {
            "fatigue_score": float(result)
        }

    # =================================================
    # RAG
    # =================================================

    def run_rag(
        self,
        query: str
    ) -> Dict[str, Any]:

        if self.rag_pipeline is None:

            print(
                "Member B RAG pipeline unavailable."
            )

            return {
                "context": [],
                "evidence": [],
                "answer": ""
            }

        if hasattr(
            self.rag_pipeline,
            "run"
        ):

            result = self.rag_pipeline.run(
                query
            )

        elif hasattr(
            self.rag_pipeline,
            "query"
        ):

            result = self.rag_pipeline.query(
                query
            )

        else:

            raise AttributeError(
                "RAGPipeline must have "
                "run() or query()."
            )

        if isinstance(result, dict):

            return result

        return {
            "context": [],
            "evidence": [],
            "answer": str(result)
        }

    # =================================================
    # RECOMMENDATION
    # =================================================

    def generate_recommendation(
        self,
        fatigue_data: Dict[str, Any],
        rag_data: Dict[str, Any]
    ) -> str:

        # If RecommendationAgent is unavailable,
        # use the built-in fallback recommendation.

        if self.recommendation_agent is None:

            return self._default_recommendation(
                fatigue_data
            )

        payload = {
            "fatigue": fatigue_data,
            "knowledge": rag_data
        }

        if hasattr(
            self.recommendation_agent,
            "run"
        ):

            result = (
                self.recommendation_agent.run(
                    payload
                )
            )

        elif hasattr(
            self.recommendation_agent,
            "recommend"
        ):

            result = (
                self.recommendation_agent.recommend(
                    payload
                )
            )

        else:

            return self._default_recommendation(
                fatigue_data
            )

        if isinstance(result, dict):

            return str(
                result.get(
                    "recommendation",
                    result
                )
            )

        return str(result)

    # =================================================
    # FALLBACK RECOMMENDATION
    # =================================================

    @staticmethod
    def _default_recommendation(
        fatigue_data: Dict[str, Any]
    ) -> str:

        score = float(
            fatigue_data.get(
                "fatigue_score",
                0
            )
        )

        if score >= 75:

            return (
                "High fatigue detected. "
                "Take a rest break and avoid "
                "activities requiring prolonged "
                "attention."
            )

        if score >= 40:

            return (
                "Moderate fatigue detected. "
                "Consider taking a short break "
                "and getting adequate rest."
            )

        return (
            "Low fatigue detected. "
            "Continue normal activities while "
            "maintaining healthy rest habits."
        )