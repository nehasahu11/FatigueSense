from pathlib import Path

from backend.app.agents.image_analysis_agent import ImageAnalysisAgent
from backend.app.agents.fatigue_scoring_agent import FatigueScoringAgent


# =========================================================
# Configuration
# =========================================================

MODEL_DIR = "backend/data/models"
IMAGE_DIR = Path("backend/data/test_images")

TEST_IMAGES = [
    "image_1_rested.png",
    "image_2_mild_fatigue.png",
    "image_3_high_fatigue.png",
    "image_4_edge_case.png",
]


# =========================================================
# Helpers
# =========================================================

def validate_cv_features(features: dict) -> None:
    """
    Validate the output produced by ImageAnalysisAgent.
    """

    required_fields = [
        "face_detected",
        "face_count",
        "average_ear",
        "eye_state",
        "possible_blink",
        "mouth_aspect_ratio",
        "yawn_detected",
        "dark_circle_present",
    ]

    for field in required_fields:
        assert field in features, (
            f"Missing CV feature: {field}"
        )

    assert isinstance(
        features["face_detected"],
        bool
    )

    assert features["face_count"] >= 0

    if features["average_ear"] is not None:
        assert features["average_ear"] >= 0

    if features["mouth_aspect_ratio"] is not None:
        assert features["mouth_aspect_ratio"] >= 0

    assert features["eye_state"] in {
        "open",
        "closed",
        "unknown"
    }

    assert isinstance(
        features["possible_blink"],
        bool
    )

    assert isinstance(
        features["yawn_detected"],
        bool
    )

    assert isinstance(
        features["dark_circle_present"],
        bool
    )


def validate_fatigue_result(result: dict) -> None:
    """
    Validate the output produced by FatigueScoringAgent.
    """

    required_fields = [
        "fatigue_score",
        "risk_level",
        "components",
    ]

    for field in required_fields:
        assert field in result, (
            f"Missing fatigue result field: {field}"
        )

    score = result["fatigue_score"]

    assert isinstance(score, (int, float))

    assert 0.0 <= score <= 100.0

    assert result["risk_level"] in {
        "Low",
        "Medium",
        "High"
    }

    components = result["components"]

    required_components = [
        "eye_closure_score",
        "eye_state_score",
        "blink_score",
        "yawn_score",
        "dark_circle_score",
    ]

    for component in required_components:
        assert component in components, (
            f"Missing score component: {component}"
        )

        assert isinstance(
            components[component],
            (int, float)
        )

        assert components[component] >= 0


# =========================================================
# Main Integration Test
# =========================================================

def main():

    print("=" * 70)
    print("FATIGUESENSE - CV → FATIGUE INTEGRATION TEST")
    print("=" * 70)

    # -----------------------------------------------------
    # Check configuration
    # -----------------------------------------------------

    model_dir = Path(MODEL_DIR)

    if not model_dir.exists():
        raise FileNotFoundError(
            f"Model directory not found: {model_dir}"
        )

    print("\n✓ Model directory found")

    # -----------------------------------------------------
    # Create agents
    # -----------------------------------------------------

    image_agent = ImageAnalysisAgent(
        model_directory=MODEL_DIR
    )

    scoring_agent = FatigueScoringAgent()

    passed = 0
    failed = 0

    # -----------------------------------------------------
    # Test every current testing image
    # -----------------------------------------------------

    for image_name in TEST_IMAGES:

        print("\n" + "-" * 70)
        print(f"Testing: {image_name}")
        print("-" * 70)

        image_path = IMAGE_DIR / image_name

        try:

            # ---------------------------------------------
            # 1. Check image
            # ---------------------------------------------

            if not image_path.exists():
                raise FileNotFoundError(
                    f"Image not found: {image_path}"
                )

            print(
                f"✓ Image exists "
                f"({image_path.stat().st_size:,} bytes)"
            )

            # ---------------------------------------------
            # 2. Image → CV features
            # ---------------------------------------------

            cv_features = image_agent.analyze(
                str(image_path)
            )

            print("✓ ImageAnalysisAgent completed")

            # ---------------------------------------------
            # 3. Validate CV contract
            # ---------------------------------------------

            validate_cv_features(
                cv_features
            )

            print("✓ CV feature contract valid")

            # ---------------------------------------------
            # 4. CV features → fatigue result
            # ---------------------------------------------

            fatigue_result = scoring_agent.score(
                cv_features
            )

            print("✓ FatigueScoringAgent completed")

            # ---------------------------------------------
            # 5. Validate fatigue contract
            # ---------------------------------------------

            validate_fatigue_result(
                fatigue_result
            )

            print("✓ Fatigue result contract valid")

            # ---------------------------------------------
            # 6. Display integration output
            # ---------------------------------------------

            print("\nINTEGRATION OUTPUT")
            print("-" * 40)

            print(
                "Image          :",
                image_name
            )

            print(
                "Face Detected  :",
                cv_features["face_detected"]
            )

            print(
                "Face Count     :",
                cv_features["face_count"]
            )

            print(
                "Eye State      :",
                cv_features["eye_state"]
            )

            print(
                "Average EAR    :",
                cv_features["average_ear"]
            )

            print(
                "Blink          :",
                cv_features["possible_blink"]
            )

            print(
                "Yawn           :",
                cv_features["yawn_detected"]
            )

            print(
                "Mouth MAR      :",
                cv_features["mouth_aspect_ratio"]
            )

            print(
                "Dark Circle    :",
                cv_features["dark_circle_present"]
            )

            print(
                "Fatigue Score  :",
                fatigue_result["fatigue_score"]
            )

            print(
                "Risk Level     :",
                fatigue_result["risk_level"]
            )

            print(
                "Components     :",
                fatigue_result["components"]
            )

            print("\nSTATUS: PASS ✓")

            passed += 1

        except Exception as error:

            print("\nSTATUS: FAIL ✗")
            print(
                f"Error: {type(error).__name__}: {error}"
            )

            failed += 1

    # -----------------------------------------------------
    # Final summary
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("CV → FATIGUE INTEGRATION TEST SUMMARY")
    print("=" * 70)

    print(
        f"Tests Passed : {passed}/{len(TEST_IMAGES)}"
    )

    print(
        f"Tests Failed : {failed}/{len(TEST_IMAGES)}"
    )

    print("-" * 70)

    if failed == 0:

        print(
            "ALL CV → FATIGUE INTEGRATION TESTS PASSED ✓"
        )

        print(
            "\nMember-A CV pipeline is ready "
            "for downstream integration."
        )

    else:

        print(
            "CV → FATIGUE INTEGRATION TEST FAILED ✗"
        )

        raise SystemExit(1)

    print("=" * 70)


if __name__ == "__main__":
    main()