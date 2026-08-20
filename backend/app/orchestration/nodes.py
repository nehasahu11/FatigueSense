from typing import Any, Dict
from uuid import uuid4

from app.orchestration.state import FatigueState
from app.orchestration.router import AgentRouter
from app.orchestration.workflow_config import (
    WorkflowConfig
)


# Create shared objects
router = AgentRouter()
config = WorkflowConfig.from_env()


# =====================================================
# NODE 1 - INITIALIZE
# =====================================================

def initialize_state(
    state: FatigueState
) -> FatigueState:

    session_id = state.get(
        "session_id"
    )

    if not session_id:

        session_id = str(
            uuid4()
        )

    return {

        **state,

        "session_id":
            session_id,

        "cv_features":
            {},

        "fatigue_analysis":
            {},

        "fatigue_score":
            0.0,

        "risk_level":
            "unknown",

        "rag_context":
            [],

        "evidence":
            [],

        "rag_recommendation":
            "",

        "previous_sessions":
            [],

        "recommendation":
            "",

        "error":
            None
    }


# =====================================================
# NODE 2 - MEMORY
# =====================================================

def load_memory(
    state: FatigueState
) -> FatigueState:

    if not config.enable_memory:

        return state

    try:

        from app.memory.memory_manager import (
            MemoryManager
        )

        memory = MemoryManager()

        history = memory.get_history(

            user_id=state.get(
                "user_id"
            ),

            limit=config.max_history
        )

        return {

            **state,

            "previous_sessions":
                history
        }

    except Exception as e:

        print(
            f"Memory loading failed: {e}"
        )

        return state


# =====================================================
# NODE 3 - MEMBER A
# =====================================================

def member_a_node(
    state: FatigueState
) -> FatigueState:

    try:

        image_path = state.get(
            "image_path"
        )

        if not image_path:

            raise ValueError(
                "image_path is required."
            )

        # ---------------------------------------------
        # Image analysis
        # ---------------------------------------------

        cv_result = (
            router.run_image_analysis(
                image_path
            )
        )

        # ---------------------------------------------
        # Fatigue scoring
        # ---------------------------------------------

        fatigue_result = (
            router.calculate_fatigue(
                cv_result
            )
        )

        score = float(
            fatigue_result.get(
                "fatigue_score",
                fatigue_result.get(
                    "score",
                    0
                )
            )
        )

        risk = fatigue_result.get(
            "risk_level"
        )

        if not risk:

            risk = calculate_risk(
                score
            )

        return {

            **state,

            "cv_features":
                cv_result,

            "fatigue_analysis":
                fatigue_result,

            "fatigue_score":
                score,

            "risk_level":
                risk
        }

    except Exception as e:

        return {

            **state,

            "error":
                f"Member A error: {str(e)}"
        }


# =====================================================
# NODE 4 - MEMBER B
# =====================================================

def member_b_node(
    state: FatigueState
) -> FatigueState:

    if not config.enable_rag:

        return state

    if state.get("error"):

        return state

    try:

        score = state.get(
            "fatigue_score",
            0
        )

        risk = state.get(
            "risk_level",
            "unknown"
        )

        query = (
            f"Fatigue score is {score}. "
            f"Risk level is {risk}. "
            "Provide evidence-based information "
            "about fatigue, warning signs, risks, "
            "rest and safety recommendations."
        )

        rag_result = router.run_rag(
            query
        )

        return {

            **state,

            "rag_context":
                rag_result.get(
                    "context",
                    []
                ),

            "evidence":
                rag_result.get(
                    "evidence",
                    []
                ),

            "rag_recommendation":
                rag_result.get(
                    "answer",
                    ""
                )
        }

    except Exception as e:

        print(
            f"Member B RAG error: {e}"
        )

        return state


# =====================================================
# NODE 5 - RECOMMENDATION
# =====================================================

def recommendation_node(
    state: FatigueState
) -> FatigueState:

    if state.get("error"):

        return state

    try:

        fatigue_data = {

            "fatigue_score":
                state.get(
                    "fatigue_score",
                    0
                ),

            "risk_level":
                state.get(
                    "risk_level",
                    "unknown"
                ),

            "features":
                state.get(
                    "cv_features",
                    {}
                ),

            "analysis":
                state.get(
                    "fatigue_analysis",
                    {}
                )
        }

        rag_data = {

            "context":
                state.get(
                    "rag_context",
                    []
                ),

            "evidence":
                state.get(
                    "evidence",
                    []
                ),

            "answer":
                state.get(
                    "rag_recommendation",
                    ""
                )
        }

        recommendation = (
            router.generate_recommendation(
                fatigue_data,
                rag_data
            )
        )

        return {

            **state,

            "recommendation":
                recommendation
        }

    except Exception as e:

        return {

            **state,

            "recommendation":
                "Unable to generate recommendation.",

            "error":
                str(e)
        }


# =====================================================
# NODE 6 - FINAL RESPONSE
# =====================================================

def final_response_node(
    state: FatigueState
) -> FatigueState:

    final_response = {

        "session_id":
            state.get(
                "session_id"
            ),

        "fatigue_score":
            round(
                float(
                    state.get(
                        "fatigue_score",
                        0
                    )
                ),
                2
            ),

        "risk_level":
            state.get(
                "risk_level",
                "unknown"
            ),

        "cv_features":
            state.get(
                "cv_features",
                {}
            ),

        "analysis":
            state.get(
                "fatigue_analysis",
                {}
            ),

        "recommendation":
            state.get(
                "recommendation",
                ""
            ),

        "evidence":
            state.get(
                "evidence",
                []
            ),

        "status":
            (
                "error"
                if state.get("error")
                else "success"
            ),

        "error":
            state.get(
                "error"
            )
    }

    return {

        **state,

        "final_response":
            final_response
    }


# =====================================================
# NODE 7 - SAVE MEMORY
# =====================================================

def save_memory_node(
    state: FatigueState
) -> FatigueState:

    if not config.enable_memory:

        return state

    try:

        from app.memory.memory_manager import (
            MemoryManager
        )

        memory = MemoryManager()

        memory.save_session(

            user_id=state.get(
                "user_id"
            ),

            session_id=state.get(
                "session_id"
            ),

            result=state.get(
                "final_response",
                {}
            )
        )

    except Exception as e:

        print(
            f"Memory saving failed: {e}"
        )

    return state


# =====================================================
# RISK CALCULATION
# =====================================================

def calculate_risk(
    score: float
) -> str:

    if score >= 75:

        return "high"

    if score >= 40:

        return "moderate"

    return "low"