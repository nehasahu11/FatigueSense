import os

from app.orchestration.workflow import (
    FatigueWorkflow
)

from app.database.mysql.connection import (
    SessionLocal
)

from app.database.mysql.crud import (
    create_analysis
)


class AnalysisService:

    def __init__(self):

        self.workflow = FatigueWorkflow()

    def analyze(
        self,
        image_path: str,
        image_filename: str = "",
        user_id: str = None
    ):

        # --------------------------------
        # Run Member A + B workflow
        # --------------------------------

        result = self.workflow.run(

            image_path=image_path,

            user_id=user_id,

            image_filename=image_filename
        )

        # --------------------------------
        # Save result to MySQL
        # --------------------------------

        if (
            os.getenv(
                "ENABLE_DATABASE",
                "true"
            ).lower() == "true"
        ):

            try:

                db = SessionLocal()

                create_analysis(

                    db=db,

                    session_id=result[
                        "session_id"
                    ],

                    user_id=user_id,

                    image_filename=image_filename,

                    fatigue_score=result[
                        "fatigue_score"
                    ],

                    risk_level=result[
                        "risk_level"
                    ],

                    recommendation=result[
                        "recommendation"
                    ],

                    evidence=result.get(
                        "evidence",
                        []
                    )
                )

                db.close()

            except Exception as e:

                print(
                    f"MySQL save failed: {e}"
                )

        return result