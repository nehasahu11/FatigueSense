class RecommendationService:

    def generate(
        self,
        fatigue_score: float,
        risk_level: str
    ):

        if risk_level == "high":

            return {
                "level": "high",

                "recommendations": [

                    "Take an immediate rest break.",

                    "Avoid driving or operating "
                    "dangerous machinery if feeling "
                    "very sleepy.",

                    "Get adequate sleep.",

                    "If fatigue is persistent, "
                    "consider professional advice."
                ]
            }

        if risk_level == "moderate":

            return {
                "level": "moderate",

                "recommendations": [

                    "Take a short break.",

                    "Stay hydrated.",

                    "Reduce prolonged screen exposure.",

                    "Maintain a regular sleep schedule."
                ]
            }

        return {
            "level": "low",

            "recommendations": [

                "Fatigue appears low.",

                "Continue maintaining healthy "
                "sleep and rest habits."
            ]
        }