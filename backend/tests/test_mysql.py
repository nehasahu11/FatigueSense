import os

import pytest

from sqlalchemy import text

from backend.app.database.mysql.connection import (
    engine,
    SessionLocal
)

from backend.app.database.mysql.models import (
    Base,
    Analysis
)


@pytest.fixture
def db():
    Base.metadata.create_all(
        bind=engine
    )

    session = SessionLocal()

    # Remove old test records before each test
    session.query(Analysis).filter(
        Analysis.session_id.in_([
            "pytest-session",
            "pytest-read-session"
        ])
    ).delete(synchronize_session=False)

    session.commit()

    try:
        yield session

    finally:
        # Roll back any failed transaction first
        session.rollback()

        # Clean up test records after the test
        session.query(Analysis).filter(
            Analysis.session_id.in_([
                "pytest-session",
                "pytest-read-session"
            ])
        ).delete(synchronize_session=False)

        session.commit()
        session.close()

def test_mysql_connection():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            assert result.scalar() == 1

    except Exception as e:

        pytest.fail(
            f"MySQL connection failed: {e}"
        )


def test_create_analysis(db):

    record = Analysis(

        session_id="pytest-session",

        user_id="pytest-user",

        image_filename="test.jpg",

        fatigue_score=50.0,

        risk_level="moderate",

        recommendation="Take a short break.",

        evidence="Test evidence"
    )

    db.add(record)

    db.commit()

    db.refresh(record)

    assert record.id is not None

    assert record.fatigue_score == 50.0


def test_read_analysis(db):

    record = Analysis(

        session_id="pytest-read-session",

        user_id="pytest-user",

        image_filename="test.jpg",

        fatigue_score=30.0,

        risk_level="low",

        recommendation="Continue normal activities.",

        evidence="Test evidence"
    )

    db.add(record)

    db.commit()

    result = (
        db.query(Analysis)
        .filter(
            Analysis.session_id
            == "pytest-read-session"
        )
        .first()
    )

    assert result is not None

    assert result.risk_level == "low"
