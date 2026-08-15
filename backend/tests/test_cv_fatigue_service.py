from pathlib import Path

from backend.app.services.cv_fatigue_service import CVFatigueService


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
# Validation
# =========================================================

def validate_service_result(result: dict) -> None:
    """
    Validate the public output returned by CVFatigueService.
    """

    # -----------------------------------------------------
    # Top-level contract
    # -----------------------------------------------------

    assert "cv_features" in result
    assert "fatigue_result" in result

    cv_features = result["cv_features"]
    fatigue_result = result["fatigue_result"]

    # -----------------------------------------------------
    # CV feature contract
    # -----------------------------------------------------

    required_cv_fields = [
        "face_detected",
        "face_count",
        "average_ear",
        "eye_state",
        "possible_blink",
        "mouth_aspect_ratio",
        "yawn_detected",
        "dark_circle_present",
    ]

    for field in required_cv_fields:
        assert field in cv_features, (
            f"Missing CV field: {field}"
        )

    assert isinstance(
        cv_features["face_detected"],
        bool
    )

    assert cv_features["face_count"] >= 0

    if cv_features["average_ear"] is not None:
        assert cv_features["average_ear"] >= 0

    if cv_features["mouth_aspect_ratio"] is not None:
        assert cv_features["mouth_aspect_ratio"] >= 0

    assert cv_features["eye_state"] in {
        "open",
        "closed",
        "unknown",
    }

    # -----------------------------------------------------
    # Fatigue result contract
    # -----------------------------------------------------

    assert "fatigue_score" in fatigue_result
    assert "risk_level" in fatigue_result
    assert "components" in fatigue_result

    score = fatigue_result["fatigue_score"]

    assert isinstance(score, (int, float))
    assert 0.0 <= score <= 100.0

    assert fatigue_result["risk_level"] in {
        "Low",
        "Medium",
        "High",
    }

    components = fatigue_result["components"]

    required_components = [
        "eye_closure_score",
        "eye_state_score",
        "blink_score",
        "yawn_score",
        "dark_circle_score",
    ]

    for component in required_components:
        assert component in components

        assert isinstance(
            components[component],
            (int, float)
        )

        assert components[component] >= 0


# =========================================================
# Main test
# =========================================================

def main():

    print("=" * 70)
    print("FATIGUESENSE - CV FATIGUE SERVICE TEST")
    print("=" * 70)

    # -----------------------------------------------------
    # Configuration check
    # -----------------------------------------------------

    model_dir = Path(MODEL_DIR)

    if not model_dir.exists():
        raise FileNotFoundError(
            f"Model directory not found: {model_dir}"
        )

    print("\n✓ Model directory found")

    # -----------------------------------------------------
    # Create service
    # -----------------------------------------------------

    service = CVFatigueService(
        model_directory=MODEL_DIR
    )

    print("✓ CVFatigueService initialized")

    passed = 0
    failed = 0

    # -----------------------------------------------------
    # Test all four images
    # -----------------------------------------------------

    for image_name in TEST_IMAGES:

        print("\n" + "-" * 70)
        print(f"Testing: {image_name}")
        print("-" * 70)

        image_path = IMAGE_DIR / image_name

        try:

            # ---------------------------------------------
            # Check image
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
            # Run complete service
            # ---------------------------------------------

            result = service.analyze(
                str(image_path)
            )

            print("✓ CVFatigueService completed")

            # ---------------------------------------------
            # Validate public contract
            # ---------------------------------------------

            validate_service_result(result)

            print("✓ Service output contract valid")

            # ---------------------------------------------
            # Extract results
            # ---------------------------------------------

            cv_features = result["cv_features"]
            fatigue_result = result["fatigue_result"]

            # ---------------------------------------------
            # Display output
            # ---------------------------------------------

            print("\nSERVICE OUTPUT")
            print("-" * 40)

            print(
                "Face Detected :",
                cv_features["face_detected"]
            )

            print(
                "Face Count    :",
                cv_features["face_count"]
            )

            print(
                "Eye State     :",
                cv_features["eye_state"]
            )

            print(
                "Average EAR   :",
                cv_features["average_ear"]
            )

            print(
                "Blink         :",
                cv_features["possible_blink"]
            )

            print(
                "Yawn          :",
                cv_features["yawn_detected"]
            )

            print(
                "Mouth MAR     :",
                cv_features["mouth_aspect_ratio"]
            )

            print(
                "Dark Circle   :",
                cv_features["dark_circle_present"]
            )

            print(
                "Fatigue Score :",
                fatigue_result["fatigue_score"]
            )

            print(
                "Risk Level    :",
                fatigue_result["risk_level"]
            )

            print(
                "Components    :",
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
    # Summary
    # -----------------------------------------------------

    print("\n")
    print("=" * 70)
    print("CV FATIGUE SERVICE TEST SUMMARY")
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
            "ALL CV FATIGUE SERVICE TESTS PASSED ✓"
        )

    else:

        print(
            "CV FATIGUE SERVICE TEST FAILED ✗"
        )

        raise SystemExit(1)

    print("=" * 70)


if __name__ == "__main__":
    main()