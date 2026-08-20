from app.orchestration.graph import run_workflow

from app.database.mysql.connection import SessionLocal
from app.database.mysql.crud import create_analysis


class AnalysisService:
    """
    Member D service responsible for running
    the LangGraph fatigue-analysis workflow
    and saving the result to MySQL.
    """

    def analyze(
        self,
        image_path: str,
        image_filename: str = "",
        user_id: str = None
    ):

        # -----------------------------------------
        # Run LangGraph workflow
        # -----------------------------------------

        result = run_workflow(

            image_path=image_path,

            image_filename=image_filename,

            user_id=user_id
        )

        # -----------------------------------------
        # Save successful result to MySQL
        # -----------------------------------------

        if result.get("status") == "success":

            db = SessionLocal()

            try:

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

                    recommendation=result.get(
                        "recommendation",
                        ""
                    ),

                    evidence=result.get(
                        "evidence",
                        []
                    )
                )

            except Exception as e:

                print(
                    f"MySQL save failed: {e}"
                )

            finally:

                db.close()

        return result