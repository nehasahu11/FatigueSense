from typing import Any, Dict


class AgentRouter:

    def __init__(self):
        self.image_agent = None
        self.fatigue_agent = None
        self.recommendation_agent = None
        self.rag_pipeline = None

        self._load_agents()

    def _load_agents(self):
        """
        Load Member A and Member B components.

        Member D does not implement their logic.
        It only calls their interfaces.
        """

        # -----------------------------
        # MEMBER A
        # -----------------------------
        try:
            from app.agents.image_analysis_agent import (
                ImageAnalysisAgent
            )

            self.image_agent = ImageAnalysisAgent()

        except Exception as e:
            print(f"Member A image agent unavailable: {e}")

        try:
            from app.agents.fatigue_scoring_agent import (
                FatigueScoringAgent
            )

            self.fatigue_agent = FatigueScoringAgent()

        except Exception as e:
            print(f"Member A fatigue agent unavailable: {e}")

        try:
            from app.agents.recommendation_agent import (
                RecommendationAgent
            )

            self.recommendation_agent = RecommendationAgent()

        except Exception as e:
            print(f"Member A recommendation agent unavailable: {e}")

        # -----------------------------
        # MEMBER B
        # -----------------------------
        try:
            from app.rag.pipeline import RAGPipeline

            self.rag_pipeline = RAGPipeline()

        except Exception as e:
            print(f"Member B RAG unavailable: {e}")

    def run_image_analysis(
        self,
        image_path: str
    ) -> Dict[str, Any]:

        if self.image_agent is None:
            raise RuntimeError(
                "Member A image analysis agent is unavailable"
            )

        if hasattr(self.image_agent, "run"):
            return self.image_agent.run(image_path)

        if hasattr(self.image_agent, "analyze"):
            return self.image_agent.analyze(image_path)

        raise AttributeError(
            "Member A ImageAnalysisAgent must provide "
            "run() or analyze()"
        )

    def calculate_fatigue(
        self,
        cv_features: Dict[str, Any]
    ) -> Dict[str, Any]:

        if self.fatigue_agent is None:
            raise RuntimeError(
                "Member A fatigue scoring agent is unavailable"
            )

        if hasattr(self.fatigue_agent, "run"):
            return self.fatigue_agent.run(cv_features)

        if hasattr(self.fatigue_agent, "score"):
            return self.fatigue_agent.score(cv_features)

        raise AttributeError(
            "Member A FatigueScoringAgent must provide "
            "run() or score()"
        )

    def get_rag_information(
        self,
        query: str
    ) -> Dict[str, Any]:

        if self.rag_pipeline is None:
            return {
                "context": [],
                "evidence": [],
                "answer": ""
            }

        if hasattr(self.rag_pipeline, "run"):
            result = self.rag_pipeline.run(query)

        elif hasattr(self.rag_pipeline, "query"):
            result = self.rag_pipeline.query(query)

        else:
            raise AttributeError(
                "Member B RAGPipeline must provide run() or query()"
            )

        if isinstance(result, dict):
            return result

        return {
            "context": [],
            "evidence": [],
            "answer": str(result)
        }

    def generate_recommendation(
        self,
        fatigue_data: Dict[str, Any],
        rag_data: Dict[str, Any]
    ) -> str:

        if self.recommendation_agent is None:
            return self._default_recommendation(
                fatigue_data
            )

        payload = {
            "fatigue": fatigue_data,
            "knowledge": rag_data
        }

        if hasattr(self.recommendation_agent, "run"):
            result = self.recommendation_agent.run(payload)

        elif hasattr(
            self.recommendation_agent,
            "recommend"
        ):
            result = self.recommendation_agent.recommend(payload)

        else:
            return self._default_recommendation(
                fatigue_data
            )

        if isinstance(result, dict):
            return result.get(
                "recommendation",
                str(result)
            )

        return str(result)

    @staticmethod
    def _default_recommendation(
        fatigue_data: Dict[str, Any]
    ) -> str:

        score = float(
            fatigue_data.get("fatigue_score", 0)
        )

        if score >= 75:
            return (
                "High fatigue detected. "
                "Take a break, rest adequately, and avoid "
                "activities requiring prolonged attention."
            )

        if score >= 40:
            return (
                "Moderate fatigue detected. "
                "Consider taking a short break and getting "
                "adequate rest."
            )

        return (
            "Low fatigue detected. "
            "Continue normal activities while maintaining "
            "healthy rest habits."
        )