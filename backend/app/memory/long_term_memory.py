from typing import Dict, Any, List


class LongTermMemory:

    def __init__(self):

        self.firestore = None

        try:

            from backend.app.database.firestore.connection import (
                get_firestore
            )

            self.firestore = get_firestore()

        except Exception as e:

            print(
                f"Firestore unavailable: {e}"
            )

    def save(
        self,
        user_id: str,
        session_id: str,
        data: Dict[str, Any]
    ):

        if not self.firestore:
            return

        if not user_id:
            return

        try:

            collection = (
                self.firestore
                .collection("users")
                .document(user_id)
                .collection("fatigue_sessions")
            )

            collection.document(
                session_id
            ).set(data)

        except Exception as e:

            print(
                f"Long-term memory save error: {e}"
            )

    def get_history(
        self,
        user_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:

        if not self.firestore:
            return []

        if not user_id:
            return []

        try:

            collection = (
                self.firestore
                .collection("users")
                .document(user_id)
                .collection("fatigue_sessions")
            )

            docs = (
                collection
                .order_by(
                    "created_at",
                    direction="DESCENDING"
                )
                .limit(limit)
                .stream()
            )

            return [
                doc.to_dict()
                for doc in docs
            ]

        except Exception as e:

            print(
                f"History retrieval error: {e}"
            )

            return []
