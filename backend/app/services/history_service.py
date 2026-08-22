from backend.app.database.mysql.connection import (
    SessionLocal
)

from backend.app.database.mysql.crud import (
    get_user_history,
    get_analysis
)


class HistoryService:

    def get_history(
        self,
        user_id,
        limit=20
    ):

        db = SessionLocal()

        try:

            records = get_user_history(
                db,
                user_id,
                limit
            )

            return [
                {
                    "session_id":
                        r.session_id,

                    "fatigue_score":
                        r.fatigue_score,

                    "risk_level":
                        r.risk_level,

                    "recommendation":
                        r.recommendation,

                    "created_at":
                        r.created_at
                }
                for r in records
            ]

        finally:

            db.close()

    def get_analysis(
        self,
        session_id
    ):

        db = SessionLocal()

        try:

            record = get_analysis(
                db,
                session_id
            )

            if not record:
                return None

            return {
                "session_id":
                    record.session_id,

                "fatigue_score":
                    record.fatigue_score,

                "risk_level":
                    record.risk_level,

                "recommendation":
                    record.recommendation,

                "created_at":
                    record.created_at
            }

        finally:

            db.close()
