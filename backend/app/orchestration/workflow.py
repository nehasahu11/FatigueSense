from pathlib import Path
from typing import Any, Dict, Optional

from backend.app.memory.session_memory import AnalysisState
from backend.app.agents.image_analysis_agent import ImageAnalysisAgent
from backend.app.agents.fatigue_scoring_agent import FatigueScoringAgent
from backend.app.rag.pipeline import RAGPipeline


class FatigueWorkflow:
    """
    Main orchestration workflow for FatigueSense.

    Current pipeline:

        Image
          ↓
        ImageAnalysisAgent
          ↓
        CV Features
          ↓
        RAG Pipeline
          ↓
        FatigueScoringAgent
          ↓
        Final Fatigue Result

    Recommendation and history persistence are not included
    yet because their implementations are not currently
    available in the integrated branch.
    """

    def __init__(
        self,
        model_directory: Optional[str] = None,
        rag_pipeline: Optional[RAGPipeline] = None,
    ):
        """
        Initialize the FatigueSense workflow.

        Args:
            model_directory:
                Directory containing the MediaPipe model files.

                Default:
                    backend/data/models

            rag_pipeline:
                Optional RAGPipeline instance.
                Useful for testing and dependency injection.
        """

        # =====================================================
        # 1. Resolve model directory
        # =====================================================

        if model_directory is None:
            project_root = Path(__file__).resolve().parents[2]

            model_directory = str(
                project_root / "data" / "models"
            )

        self.model_directory = Path(model_directory)

        # =====================================================
        # 2. Validate model directory
        # =====================================================

        if not self.model_directory.exists():
            raise FileNotFoundError(
                f"Model directory not found: "
                f"{self.model_directory}"
            )

        if not self.model_directory.is_dir():
            raise NotADirectoryError(
                f"Model path is not a directory: "
                f"{self.model_directory}"
            )

        # =====================================================
        # 3. Initialize Image Analysis Agent
        # =====================================================

        self.image_agent = ImageAnalysisAgent(
            model_directory=str(
                self.model_directory
            )
        )

        # =====================================================
        # 4. Initialize Fatigue Scoring Agent
        # =====================================================

        self.scoring_agent = FatigueScoringAgent()

        # =====================================================
        # 5. Initialize RAG Pipeline
        # =====================================================

        self.rag_pipeline = (
            rag_pipeline
            if rag_pipeline is not None
            else RAGPipeline()
        )

    # =========================================================
    # MAIN WORKFLOW
    # =========================================================

    def analyze(
        self,
        user_id: str,
        image_path: str,
        image_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run the complete FatigueSense analysis workflow.

        Steps:

            1. Create analysis state
            2. Analyze image
            3. Retrieve relevant RAG context
            4. Calculate fatigue score
            5. Return final result

        Args:
            user_id:
                ID of the user performing the analysis.

            image_path:
                Path to the image being analyzed.

            image_name:
                Original image filename.

        Returns:
            Dictionary containing the analysis result.
        """

        # =====================================================
        # 1. Create analysis state
        # =====================================================

        state = AnalysisState(
            user_id=user_id,
            image_path=image_path,
            image_name=image_name,
        )

        print(
            "\n========== FATIGUESENSE WORKFLOW =========="
        )

        try:

            # =================================================
            # STEP 1 — IMAGE ANALYSIS
            # =================================================

            print(
                "[1/4] Running ImageAnalysisAgent..."
            )

            features = self.image_agent.analyze(
                image_path
            )

            state.features = features

            print(
                "CV features extracted successfully."
            )

            # =================================================
            # STEP 2 — RAG RETRIEVAL
            # =================================================

            print(
                "[2/4] Running RAG pipeline..."
            )

            rag_query = self._build_rag_query(
                features
            )

            rag_result = self.rag_pipeline.search(
                query=rag_query,
                top_k=5,
            )

            # RAGPipeline.search() returns:
            #
            # {
            #     "ids": [...],
            #     "documents": [...],
            #     "metadatas": [...],
            #     "scores": [...]
            # }
            #
            # Therefore use "documents".

            state.rag_context = rag_result.get(
                "documents",
                [],
            )

            print(
                f"RAG context retrieved: "
                f"{len(state.rag_context)} documents."
            )

            # =================================================
            # STEP 3 — FATIGUE SCORING
            # =================================================

            print(
                "[3/4] Running FatigueScoringAgent..."
            )

            scoring_result = self.scoring_agent.score(
                features
            )

            state.fatigue_score = (
                scoring_result["fatigue_score"]
            )

            state.risk_level = (
                scoring_result["risk_level"]
            )

            print(
                f"Fatigue Score: "
                f"{state.fatigue_score}"
            )

            print(
                f"Risk Level: "
                f"{state.risk_level}"
            )

            # =================================================
            # STEP 4 — FINAL RESULT
            # =================================================

            print(
                "[4/4] Preparing final result..."
            )

            result = {
                "success": True,
                "user_id": state.user_id,
                "image_name": state.image_name,
                "fatigue_score": state.fatigue_score,
                "risk_level": state.risk_level,
                "features": state.features,
                "rag_context": state.rag_context,
                "components": scoring_result.get(
                    "components",
                    {},
                ),
            }

            print(
                "========== WORKFLOW COMPLETE ==========\n"
            )

            return result

        except Exception as e:

            # =================================================
            # ERROR HANDLING
            # =================================================

            state.error = str(e)

            print(
                "WORKFLOW ERROR:",
                e,
            )

            return {
                "success": False,
                "user_id": state.user_id,
                "image_name": state.image_name,
                "error": str(e),
            }

    # =========================================================
    # RAG QUERY BUILDER
    # =========================================================

    def _build_rag_query(
        self,
        features: Dict[str, Any],
    ) -> str:
        """
        Convert CV features into a text query for RAG.

        RAGPipeline.search() expects a string query.
        ImageAnalysisAgent returns a feature dictionary,
        so the relevant features are converted into a
        descriptive query.
        """

        query_parts = []

        # =====================================================
        # Eye state
        # =====================================================

        eye_state = features.get(
            "eye_state"
        )

        if eye_state:
            query_parts.append(
                f"eye state {eye_state}"
            )

        # =====================================================
        # Eye Aspect Ratio
        # =====================================================

        average_ear = features.get(
            "average_ear"
        )

        if average_ear is not None:
            query_parts.append(
                f"eye aspect ratio {average_ear}"
            )

        # =====================================================
        # Eye closure
        # =====================================================

        if features.get(
            "both_eyes_closed",
            False,
        ):
            query_parts.append(
                "both eyes closed"
            )

        elif (
            features.get(
                "left_eye_closed",
                False,
            )
            or features.get(
                "right_eye_closed",
                False,
            )
        ):
            query_parts.append(
                "eye closure"
            )

        # =====================================================
        # Possible blink
        # =====================================================

        if features.get(
            "possible_blink",
            False,
        ):
            query_parts.append(
                "possible blink"
            )

        # =====================================================
        # Mouth Aspect Ratio
        # =====================================================

        mouth_aspect_ratio = features.get(
            "mouth_aspect_ratio"
        )

        if mouth_aspect_ratio is not None:
            query_parts.append(
                f"mouth aspect ratio "
                f"{mouth_aspect_ratio}"
            )

        # =====================================================
        # Yawning
        # =====================================================

        if features.get(
            "yawn_detected",
            False,
        ):
            query_parts.append(
                "yawning fatigue"
            )

        # =====================================================
        # Under-eye darkness
        # =====================================================

        darkness = features.get(
            "average_under_eye_darkness"
        )

        if darkness is not None:
            query_parts.append(
                f"under eye darkness {darkness}"
            )

        # =====================================================
        # Dark circles
        # =====================================================

        if features.get(
            "dark_circle_present",
            False,
        ):
            query_parts.append(
                "dark circles"
            )

        # =====================================================
        # Fallback query
        # =====================================================

        if not query_parts:
            return (
                "fatigue assessment based on "
                "facial and eye features"
            )

        return (
            "fatigue assessment "
            + " ".join(query_parts)
        )

    # =========================================================
    # RESOURCE CLEANUP
    # =========================================================

    def close(self):
        """
        Release resources used by the image analysis pipeline.
        """

        if self.image_agent is not None:
            self.image_agent.close()