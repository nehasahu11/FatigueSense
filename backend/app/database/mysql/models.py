from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Analysis(Base):

    __tablename__ = "analysis"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    session_id = Column(
        String(100),
        unique=True,
        nullable=False
    )

    user_id = Column(
        String(100),
        nullable=True,
        index=True
    )

    image_filename = Column(
        String(255)
    )

    fatigue_score = Column(
        Float
    )

    risk_level = Column(
        String(50)
    )

    recommendation = Column(
        Text
    )

    evidence = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )