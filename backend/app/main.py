from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.app.orchestration.workflow import FatigueWorkflow


# ============================================================
# APPLICATION
# ============================================================

app = FastAPI(
    title="FatigueSense API",
    description="AI-powered fatigue analysis backend",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE_DIR / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# IN-MEMORY HISTORY
# ============================================================

history_store: Dict[str, List[Dict[str, Any]]] = {}

MAX_HISTORY = 20


# ============================================================
# WORKFLOW
# ============================================================

workflow = FatigueWorkflow()


# ============================================================
# HELPERS
# ============================================================

def build_recommendation(
    fatigue_score: float,
    risk_level: str,
) -> str:
    """
    Provide a safe fallback recommendation for the frontend.
    """

    if risk_level == "High":
        return (
            "Your fatigue indicators are high. Take a break, "
            "rest properly, and avoid demanding activities until "
            "you feel sufficiently alert."
        )

    if risk_level == "Medium":
        return (
            "Your fatigue indicators are moderate. Consider "
            "taking a short break, staying hydrated, and getting "
            "adequate rest before continuing demanding activities."
        )

    return (
        "Your fatigue indicators are currently low. Continue "
        "maintaining healthy sleep, hydration, and regular breaks."
    )


def build_signals(
    workflow_result: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Convert workflow scoring components into the structure
    expected by the React SignalBreakdown component.
    """

    components = workflow_result.get(
        "components",
        {},
    )

    signal_definitions = [
        (
            "eye_closure",
            "Eye Closure",
            "Fatigue contribution based on the detected eye closure signal.",
            "eye_closure_score",
            35.0,
        ),
        (
            "eye_state",
            "Eye State",
            "Supporting fatigue signal based on whether the eyes appear open or closed.",
            "eye_state_score",
            15.0,
        ),
        (
            "blink",
            "Blink / Eye Closure",
            "Supporting signal from the eye-closure and blink detector.",
            "blink_score",
            10.0,
        ),
        (
            "yawn",
            "Yawn",
            "Fatigue contribution based on mouth opening and detected yawning.",
            "yawn_score",
            25.0,
        ),
        (
            "under_eye_darkness",
            "Under-Eye Darkness",
            "Supporting signal based on detected under-eye darkness.",
            "dark_circle_score",
            15.0,
        ),
    ]

    signals = []

    for (
        key,
        label,
        description,
        component_key,
        maximum,
    ) in signal_definitions:

        raw_value = float(
            components.get(
                component_key,
                0.0,
            )
        )

        normalized = (
            raw_value / maximum * 100.0
            if maximum > 0
            else 0.0
        )

        normalized = max(
            0.0,
            min(100.0, normalized),
        )

        signals.append(
            {
                "key": key,
                "label": label,
                "value": round(
                    normalized,
                    2,
                ),
                "description": description,
            }
        )

    return signals


def aggregate_results(
    user_id: str,
    image_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Combine the results from multiple uploaded images.

    Each image is analyzed independently and the fatigue
    score is averaged.
    """

    successful_results = [
        result
        for result in image_results
        if result.get("success") is True
    ]

    if not successful_results:
        raise HTTPException(
            status_code=422,
            detail=(
                "No uploaded image could be analyzed successfully."
            ),
        )

    scores = [
        float(
            result["fatigue_score"]
        )
        for result in successful_results
    ]

    average_score = round(
        mean(scores),
        2,
    )

    if average_score <= 33:
        risk_level = "Low"

    elif average_score <= 66:
        risk_level = "Medium"

    else:
        risk_level = "High"

    # Use the first successful result as the source
    # for signal/component information.

    representative = successful_results[0]

    signals = build_signals(
        representative
    )

    recommendation = build_recommendation(
        average_score,
        risk_level,
    )

    created_at = datetime.now(
        timezone.utc
    ).isoformat()

    result = {
        "success": True,
        "user_id": user_id,
        "fatigue_score": average_score,
        "risk_level": risk_level,
        "recommendation": recommendation,
        "signals": signals,
        "created_at": created_at,

        "images_analyzed": len(
            successful_results
        ),

        "image_names": [
            result.get("image_name")
            for result in successful_results
        ],

        "analyses": successful_results,
    }

    return result


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "name": "FatigueSense API",
        "status": "running",
        "version": "1.0.0",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "FatigueSense",
    }


# ============================================================
# ANALYZE
# ============================================================

@app.post("/analyze")
async def analyze(
    user_id: str = Form(...),
    images: List[UploadFile] = File(...),
):
    """
    Analyze 3-4 uploaded images.
    """

    # ========================================================
    # VALIDATE USER ID
    # ========================================================

    user_id = user_id.strip()

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="user_id is required.",
        )

    # ========================================================
    # VALIDATE IMAGE COUNT
    # ========================================================

    if len(images) < 3 or len(images) > 4:
        raise HTTPException(
            status_code=400,
            detail="Please upload between 3 and 4 images.",
        )

    image_results: List[Dict[str, Any]] = []
    saved_files: List[Path] = []

    try:

        # ====================================================
        # SAVE AND ANALYZE EVERY UPLOADED IMAGE
        # ====================================================

        for index, image in enumerate(images):

            # ------------------------------------------------
            # Validate filename
            # ------------------------------------------------

            if not image.filename:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Image {index + 1} has no filename."
                    ),
                )

            filename = Path(
                image.filename
            ).name

            # ------------------------------------------------
            # Validate extension
            # ------------------------------------------------

            extension = Path(
                filename
            ).suffix.lower()

            if extension not in {
                ".jpg",
                ".jpeg",
                ".png",
            }:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Unsupported image format: {filename}. "
                        "Only JPG, JPEG and PNG are supported."
                    ),
                )

            # ------------------------------------------------
            # Create safe filename
            # ------------------------------------------------

            safe_name = (
                f"{user_id}_"
                f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}_"
                f"{index}"
                f"{extension}"
            )

            file_path = UPLOAD_DIR / safe_name

            # ------------------------------------------------
            # Read image
            # ------------------------------------------------

            contents = await image.read()

            if not contents:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Image {index + 1} is empty."
                    ),
                )

            # ------------------------------------------------
            # 10 MB limit
            # ------------------------------------------------

            if len(contents) > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=413,
                    detail=(
                        f"Image {index + 1} exceeds "
                        "the 10 MB limit."
                    ),
                )

            # ------------------------------------------------
            # Save image
            # ------------------------------------------------

            file_path.write_bytes(contents)

            saved_files.append(file_path)

            # =================================================
            # RUN WORKFLOW
            # =================================================

            print(
                f"\n[API] Analyzing image "
                f"{index + 1}/{len(images)}: "
                f"{filename}"
            )

            workflow_result = workflow.analyze(
                user_id=user_id,
                image_path=str(file_path),
                image_name=filename,
            )

            # =================================================
            # IMPORTANT:
            # STOP ENTIRE ANALYSIS IF IMAGE IS INVALID
            # =================================================

            if not workflow_result.get("success"):

                error_message = workflow_result.get(
                    "error",
                    "Image analysis failed.",
                )

                print(
                    f"[API] Image analysis failed: "
                    f"{error_message}"
                )

                raise HTTPException(
                    status_code=422,
                    detail=error_message,
                )

            image_results.append(
                workflow_result
            )

        # ====================================================
        # AGGREGATE RESULTS
        # ====================================================

        result = aggregate_results(
            user_id=user_id,
            image_results=image_results,
        )

        # ====================================================
        # SAVE HISTORY
        # ====================================================

        user_history = history_store.setdefault(
            user_id,
            [],
        )

        user_history.insert(
            0,
            result,
        )

        history_store[user_id] = user_history[
            :MAX_HISTORY
        ]

        # ====================================================
        # RETURN RESULT
        # ====================================================

        return {
            "result": result
        }

    except HTTPException:
        raise

    except Exception as exc:

        print(
            f"[API] Analysis error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(exc)}",
        )

    finally:

        # ====================================================
        # REMOVE TEMPORARY UPLOADED FILES
        # ====================================================

        for file_path in saved_files:

            try:

                if file_path.exists():
                    file_path.unlink()

            except Exception as cleanup_error:

                print(
                    f"[API] Could not remove temporary file "
                    f"{file_path}: {cleanup_error}"
                )


# ============================================================
# HISTORY
# ============================================================

@app.get("/history")
def get_history(
    user_id: str,
):
    """
    Return the latest analysis results for a user.
    """

    user_id = user_id.strip()

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="user_id is required.",
        )

    return {
        "history": history_store.get(
            user_id,
            [],
        )
    }


# ============================================================
# SHUTDOWN
# ============================================================

@app.on_event("shutdown")
def shutdown():
    """
    Release workflow resources when the API shuts down.
    """

    try:

        workflow.close()

    except Exception as exc:

        print(
            f"[API] Workflow cleanup warning: {exc}"
        )