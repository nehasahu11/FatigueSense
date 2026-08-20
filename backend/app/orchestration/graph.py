from typing import Dict, Any

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.orchestration.state import FatigueState

from app.orchestration.nodes import (
    initialize_state,
    load_memory,
    member_a_node,
    member_b_node,
    recommendation_node,
    final_response_node,
    save_memory_node
)


def build_graph():

    # Create LangGraph
    builder = StateGraph(
        FatigueState
    )

    # ---------------------------------------------
    # Add nodes
    # ---------------------------------------------

    builder.add_node(
        "initialize",
        initialize_state
    )

    builder.add_node(
        "memory",
        load_memory
    )

    builder.add_node(
        "member_a",
        member_a_node
    )

    builder.add_node(
        "member_b",
        member_b_node
    )

    builder.add_node(
        "recommendation",
        recommendation_node
    )

    builder.add_node(
        "final_response",
        final_response_node
    )

    builder.add_node(
        "save_memory",
        save_memory_node
    )

    # ---------------------------------------------
    # Add edges
    # ---------------------------------------------

    builder.add_edge(
        START,
        "initialize"
    )

    builder.add_edge(
        "initialize",
        "memory"
    )

    builder.add_edge(
        "memory",
        "member_a"
    )

    builder.add_edge(
        "member_a",
        "member_b"
    )

    builder.add_edge(
        "member_b",
        "recommendation"
    )

    builder.add_edge(
        "recommendation",
        "final_response"
    )

    builder.add_edge(
        "final_response",
        "save_memory"
    )

    builder.add_edge(
        "save_memory",
        END
    )

    # Compile graph
    return builder.compile()


# Create compiled application
fatigue_graph = build_graph()


def run_workflow(
    image_path: str,
    user_id: str = None,
    image_filename: str = "",
    session_id: str = None
) -> Dict[str, Any]:
    """
    Execute the complete FatigueSense LangGraph workflow.
    """

    initial_state: FatigueState = {

        "session_id":
            session_id or "",

        "user_id":
            user_id,

        "image_path":
            image_path,

        "image_filename":
            image_filename
    }

    result = fatigue_graph.invoke(
        initial_state
    )

    return result.get(
        "final_response",
        {
            "status": "error",
            "error":
                "Workflow did not return a response."
        }
    )