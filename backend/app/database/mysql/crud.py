import json

from app.database.mysql.models import Analysis


def create_analysis(
    db,
    session_id,
    user_id,
    image_filename,
    fatigue_score,
    risk_level,
    recommendation,
    evidence
):

    record = Analysis(

        session_id=session_id,

        user_id=user_id,

        image_filename=image_filename,

        fatigue_score=fatigue_score,

        risk_level=risk_level,

        recommendation=recommendation,

        evidence=json.dumps(
            evidence
        )
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    return record


def get_analysis(
    db,
    session_id
):

    return (
        db.query(Analysis)
        .filter(
            Analysis.session_id
            == session_id
        )
        .first()
    )


def get_user_history(
    db,
    user_id,
    limit=20
):

    return (
        db.query(Analysis)
        .filter(
            Analysis.user_id
            == user_id
        )
        .order_by(
            Analysis.created_at.desc()
        )
        .limit(limit)
        .all()
    )


def delete_analysis(
    db,
    session_id
):

    record = get_analysis(
        db,
        session_id
    )

    if record:

        db.delete(record)

        db.commit()

        return True

    return False