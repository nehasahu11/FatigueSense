from datetime import datetime


def create_session_document(
    user_id,
    session_id,
    result
):

    return {

        "user_id":
            user_id,

        "session_id":
            session_id,

        "fatigue_score":
            result.get(
                "fatigue_score",
                0
            ),

        "risk_level":
            result.get(
                "risk_level",
                "unknown"
            ),

        "recommendation":
            result.get(
                "recommendation",
                ""
            ),

        "evidence":
            result.get(
                "evidence",
                []
            ),

        "created_at":
            datetime.utcnow()
    }