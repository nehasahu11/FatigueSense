class ContextManager:

    def create_context(
        self,
        current_result: dict,
        history: list
    ) -> dict:

        previous_scores = [
            item.get(
                "fatigue_score",
                0
            )
            for item in history
        ]

        return {

            "current_score":
                current_result.get(
                    "fatigue_score",
                    0
                ),

            "current_risk":
                current_result.get(
                    "risk_level",
                    "unknown"
                ),

            "previous_scores":
                previous_scores,

            "session_count":
                len(history)
        }

    def calculate_trend(
        self,
        scores: list
    ) -> str:

        if len(scores) < 2:
            return "insufficient_data"

        if scores[-1] > scores[-2]:
            return "increasing"

        if scores[-1] < scores[-2]:
            return "decreasing"

        return "stable"