from app.database.firestore.connection import (
    get_firestore
)


def save_session(
    user_id,
    session_id,
    data
):

    db = get_firestore()

    ref = (
        db.collection("users")
        .document(user_id)
        .collection("fatigue_sessions")
        .document(session_id)
    )

    ref.set(data)

    return True


def get_session(
    user_id,
    session_id
):

    db = get_firestore()

    ref = (
        db.collection("users")
        .document(user_id)
        .collection("fatigue_sessions")
        .document(session_id)
    )

    document = ref.get()

    if document.exists:
        return document.to_dict()

    return None


def get_sessions(
    user_id,
    limit=20
):

    db = get_firestore()

    collection = (
        db.collection("users")
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