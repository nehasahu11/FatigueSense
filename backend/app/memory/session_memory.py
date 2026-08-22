from typing import Dict, List, Any


class SessionMemory:

    def __init__(self):

        self.sessions: Dict[
            str,
            List[Dict[str, Any]]
        ] = {}

    def add(
        self,
        user_id: str,
        session: Dict[str, Any]
    ):

        if not user_id:
            return

        if user_id not in self.sessions:
            self.sessions[user_id] = []

        self.sessions[user_id].append(
            session
        )

        # Keep only recent sessions
        self.sessions[user_id] = (
            self.sessions[user_id][-10:]
        )

    def get(
        self,
        user_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:

        if not user_id:
            return []

        return self.sessions.get(
            user_id,
            []
        )[-limit:]