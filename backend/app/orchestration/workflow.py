from memory.session_memory import AnalysisState
from memory.history_store import HistoryStore

from agents.image_agent import ImageAnalysisAgent
from agents.scoring_agent import FatigueScoringAgent
from agents.recommendation_agent import RecommendationAgent

from rag.pipeline import RAGPipeline


class FatigueWorkflow:

    def __init__(self):

        # Member A
        self.image_agent = ImageAnalysisAgent()
        self.scoring_agent = FatigueScoringAgent()

        # Recommendation agent
        self.recommendation_agent = RecommendationAgent()

        # Member B
        self.rag_pipeline = RAGPipeline()

        # Member D
        self.history_store = HistoryStore()

    def analyze(self, user_id, image_path, image_name):

        # --------------------------------
        # 1. Create short-term memory
        # --------------------------------

        state = AnalysisState(
            user_id=user_id,
            image_path=image_path,
            image_name=image_name
        )

        print("\n========== FATIGUESENSE WORKFLOW ==========")

        try:

            # --------------------------------
            # 2. Image Analysis
            # --------------------------------

            print("[1/5] Running ImageAnalysisAgent...")

            features = self.image_agent.analyze(image_path)

            state.features = features

            print("Features:", features)

            # --------------------------------
            # 3. RAG Retrieval
            # --------------------------------

            print("[2/5] Running RAG pipeline...")

            rag_context = self.rag_pipeline.search(features)

            state.rag_context = rag_context

            print("RAG context retrieved.")

            # --------------------------------
            # 4. Fatigue Scoring
            # --------------------------------

            print("[3/5] Running FatigueScoringAgent...")

            scoring_result = self.scoring_agent.score(features)

            state.fatigue_score = scoring_result["fatigue_score"]
            state.risk_level = scoring_result["risk_level"]

            print(
                "Score:",
                state.fatigue_score,
                "Risk:",
                state.risk_level
            )

            # --------------------------------
            # 5. Recommendation
            # --------------------------------

            print("[4/5] Generating recommendation...")

            recommendation = self.recommendation_agent.generate(
                fatigue_score=state.fatigue_score,
                risk_level=state.risk_level,
                rag_context=state.rag_context
            )

            state.recommendation = recommendation

            print("Recommendation:", recommendation)

            # --------------------------------
            # 6. Save to MySQL
            # --------------------------------

            print("[5/5] Saving result to MySQL...")

            saved = self.history_store.save_result(
                user_id=state.user_id,
                image_name=state.image_name,
                fatigue_score=state.fatigue_score,
                risk_level=state.risk_level,
                recommendation=state.recommendation
            )

            if not saved:
                print("Warning: Result could not be saved.")

            print("========== WORKFLOW COMPLETE ==========\n")

            # --------------------------------
            # Final response
            # --------------------------------

            return {
                "success": True,
                "user_id": state.user_id,
                "image_name": state.image_name,
                "fatigue_score": state.fatigue_score,
                "risk_level": state.risk_level,
                "recommendation": state.recommendation
            }

        except Exception as e:

            state.error = str(e)

            print("WORKFLOW ERROR:", e)

            return {
                "success": False,
                "error": str(e)
            }
        