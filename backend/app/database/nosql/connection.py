import os

import firebase_admin

from firebase_admin import (
    credentials,
    firestore
)


_initialized = False


def get_firestore():

    global _initialized

    if not _initialized:

        credential_path = os.getenv(
            "FIREBASE_CREDENTIALS"
        )

        if not credential_path:

            raise RuntimeError(
                "FIREBASE_CREDENTIALS is not configured"
            )

        cred = credentials.Certificate(
            credential_path
        )

        firebase_admin.initialize_app(
            cred
        )

        _initialized = True

    return firestore.client()