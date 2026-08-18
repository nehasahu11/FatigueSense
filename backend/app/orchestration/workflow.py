from pathlib import Path
from typing import Any, Dict, Optional

from backend.app.memory.session_memory import AnalysisState
from backend.app.agents.image_analysis_agent import ImageAnalysisAgent
from backend.app.agents.fatigue_scoring_agent import FatigueScoringAgent
from backend.app.rag.pipeline import RAGPipeline


class FatigueWorkflow:
    """
    Main orchestration workflow for FatigueSense.

    Pipeline:

        Image
          ↓
        ImageAnalysisAgent
          ↓
        Human Face Validation
          ↓
        CV Features
          ↓
        RAG Pipeline
          ↓
        FatigueScoringAgent
          ↓
        Final Fatigue Result
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

            rag_pipeline:
                Optional RAGPipeline instance.
                Useful for testing and dependency injection.
        """

        # =====================================================
        # 1. RESOLVE MODEL DIRECTORY
        # =====================================================

        if model_directory is None:
            project_root = Path(__file__).resolve().parents[2]

            model_directory = str(
                project_root / "data" / "models"
            )

        self.model_directory = Path(model_directory)

        # =====================================================
        # 2. VALIDATE MODEL DIRECTORY
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
        # 3. INITIALIZE IMAGE ANALYSIS AGENT
        # =====================================================

        self.image_agent = ImageAnalysisAgent(
            model_directory=str(
                self.model_directory
            )
        )

        # =====================================================
        # 4. INITIALIZE FATIGUE SCORING AGENT
        # =====================================================

        self.scoring_agent = FatigueScoringAgent()

        # =====================================================
        # 5. INITIALIZE RAG PIPELINE
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
            3. Validate human face
            4. Retrieve relevant RAG context
            5. Calculate fatigue score
            6. Return final result
        """

        # =====================================================
        # 1. CREATE ANALYSIS STATE
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
            # HUMAN FACE VALIDATION
            # =================================================

            face_detected = features.get(
                "face_detected",
                False,
            )

            if not face_detected:
                error_message = (
                    "No human face detected. "
                    "Please upload a clear image containing "
                    "a human face."
                )

                state.error = error_message

                print(
                    f"WORKFLOW VALIDATION ERROR: "
                    f"{error_message}"
                )

                print(
                    "========== WORKFLOW STOPPED ==========\n"
                )

                return {
                    "success": False,
                    "user_id": state.user_id,
                    "image_name": state.image_name,
                    "error": error_message,
                }

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
        """

        query_parts = []

        # =====================================================
        # EYE STATE
        # =====================================================

        eye_state = features.get(
            "eye_state"
        )

        if eye_state:
            query_parts.append(
                f"eye state {eye_state}"
            )

        # =====================================================
        # EYE ASPECT RATIO
        # =====================================================

        average_ear = features.get(
            "average_ear"
        )

        if average_ear is not None:
            query_parts.append(
                f"eye aspect ratio {average_ear}"
            )

        # =====================================================
        # EYE CLOSURE
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
        # POSSIBLE BLINK
        # =====================================================

        if features.get(
            "possible_blink",
            False,
        ):
            query_parts.append(
                "possible blink"
            )

        # =====================================================
        # MOUTH ASPECT RATIO
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
        # YAWNING
        # =====================================================

        if features.get(
            "yawn_detected",
            False,
        ):
            query_parts.append(
                "yawning fatigue"
            )

        # =====================================================
        # UNDER-EYE DARKNESS
        # =====================================================

        darkness = features.get(
            "average_under_eye_darkness"
        )

        if darkness is not None:
            query_parts.append(
                f"under eye darkness {darkness}"
            )

        # =====================================================
        # DARK CIRCLES
        # =====================================================

        if features.get(
            "dark_circle_present",
            False,
        ):
            query_parts.append(
                "dark circles"
            )

        # =====================================================
        # FALLBACK QUERY
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