from datetime import datetime

from app.memory.session_memory import SessionMemory
from app.memory.long_term_memory import LongTermMemory


class MemoryManager:

    def __init__(self):

        self.session_memory = SessionMemory()

        self.long_term_memory = (
            LongTermMemory()
        )

    def save_session(
        self,
        user_id: str,
        session_id: str,
        result: dict
    ):

        data = {
            "session_id":
                session_id,

            "user_id":
                user_id,

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

            "created_at":
                datetime.utcnow().isoformat()
        }

        self.session_memory.add(
            user_id,
            data
        )

        self.long_term_memory.save(
            user_id,
            session_id,
            data
        )

    def get_history(
        self,
        user_id: str,
        limit: int = 5
    ):

        memory = self.session_memory.get(
            user_id,
            limit
        )

        if memory:
            return memory

        return self.long_term_memory.get_history(
            user_id,
            limit
        )