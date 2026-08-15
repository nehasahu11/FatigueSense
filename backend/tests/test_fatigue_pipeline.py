from pathlib import Path
import sys

from backend.app.agents.image_analysis_agent import ImageAnalysisAgent
from backend.app.agents.fatigue_scoring_agent import FatigueScoringAgent


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_DIR = Path("backend/data/models")
IMAGE_DIR = Path("backend/data/test_images")


TEST_CASES = [
    {
        "name": "image_1_rested.png",
        "expected_risk": "Low",
        "expected_score": 6.91,
    },
    {
        "name": "image_2_mild_fatigue.png",
        "expected_risk": "Low",
        "expected_score": 10.24,
    },
    {
        "name": "image_3_high_fatigue.png",
        "expected_risk": "High",
        "expected_score": 75.64,
    },
    {
        "name": "image_4_edge_case.png",
        "expected_risk": "Low",
        "expected_score": 0.0,
    },
]


SCORE_TOLERANCE = 0.5


VALID_RISK_LEVELS = {
    "Low",
    "Medium",
    "High",
}


REQUIRED_FEATURES = {
    "eye_state",
    "average_ear",
    "possible_blink",
    "yawn_detected",
    "mouth_aspect_ratio",
    "dark_circle_present",
}


REQUIRED_COMPONENTS = {
    "eye_closure_score",
    "eye_state_score",
    "blink_score",
    "yawn_score",
    "dark_circle_score",
}


# ============================================================
# VALIDATION HELPERS
# ============================================================

def check_score_range(score):

    assert isinstance(
        score,
        (int, float)
    ), (
        f"Fatigue score must be numeric, "
        f"got {type(score).__name__}"
    )

    assert 0.0 <= score <= 100.0, (
        f"Fatigue score outside valid range: {score}"
    )


def check_risk_level(risk_level):

    assert risk_level in VALID_RISK_LEVELS, (
        f"Invalid risk level: {risk_level}"
    )


def check_cv_features(features):

    assert isinstance(features, dict), (
        "CV features must be returned as a dictionary."
    )

    missing = REQUIRED_FEATURES - set(features.keys())

    assert not missing, (
        f"Missing CV features: {sorted(missing)}"
    )


def check_components(components, final_score):

    assert isinstance(components, dict), (
        "Score components must be a dictionary."
    )

    missing = REQUIRED_COMPONENTS - set(
        components.keys()
    )

    assert not missing, (
        f"Missing score components: {sorted(missing)}"
    )

    total = 0.0

    for component_name in REQUIRED_COMPONENTS:

        value = components[component_name]

        assert isinstance(
            value,
            (int, float)
        ), (
            f"{component_name} must be numeric."
        )

        assert value >= 0.0, (
            f"{component_name} cannot be negative: {value}"
        )

        total += float(value)

    assert abs(total - final_score) <= 0.05, (
        f"Score mismatch: "
        f"components={total:.2f}, "
        f"final_score={final_score:.2f}"
    )


def check_expected_result(
    image_name,
    result,
    expected_risk,
    expected_score
):

    fatigue_score = result["fatigue_score"]
    risk_level = result["risk_level"]

    check_score_range(
        fatigue_score
    )

    check_risk_level(
        risk_level
    )

    assert risk_level == expected_risk, (
        f"{image_name}: expected risk "
        f"{expected_risk}, got {risk_level}"
    )

    score_difference = abs(
        fatigue_score - expected_score
    )

    assert score_difference <= SCORE_TOLERANCE, (
        f"{image_name}: expected score approximately "
        f"{expected_score}, got {fatigue_score}"
    )


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def print_cv_features(features):

    print("\nCV FEATURES")
    print("-" * 40)

    print(
        f"Eye State       : "
        f"{features.get('eye_state')}"
    )

    print(
        f"Average EAR     : "
        f"{features.get('average_ear')}"
    )

    print(
        f"Blink           : "
        f"{features.get('possible_blink')}"
    )

    print(
        f"Yawn            : "
        f"{features.get('yawn_detected')}"
    )

    print(
        f"Mouth MAR       : "
        f"{features.get('mouth_aspect_ratio')}"
    )

    print(
        f"Dark Circle     : "
        f"{features.get('dark_circle_present')}"
    )


def print_fatigue_result(result):

    print("\nFATIGUE RESULT")
    print("-" * 40)

    print(
        f"Fatigue Score   : "
        f"{result['fatigue_score']}"
    )

    print(
        f"Risk Level      : "
        f"{result['risk_level']}"
    )


def print_score_components(components):

    print("\nSCORE COMPONENTS")
    print("-" * 40)

    print(
        f"Eye Closure     : "
        f"{components['eye_closure_score']}"
    )

    print(
        f"Eye State       : "
        f"{components['eye_state_score']}"
    )

    print(
        f"Blink           : "
        f"{components['blink_score']}"
    )

    print(
        f"Yawn            : "
        f"{components['yawn_score']}"
    )

    print(
        f"Dark Circle     : "
        f"{components['dark_circle_score']}"
    )


# ============================================================
# MAIN REGRESSION TEST
# ============================================================

def main():

    print("\n" + "=" * 70)
    print("FATIGUESENSE - AUTOMATED CV REGRESSION TEST")
    print("=" * 70)

    # --------------------------------------------------------
    # Check models
    # --------------------------------------------------------

    print("\nChecking project configuration...")

    assert MODEL_DIR.exists(), (
        f"Model directory not found: {MODEL_DIR}"
    )

    assert MODEL_DIR.is_dir(), (
        f"Model path is not a directory: {MODEL_DIR}"
    )

    print("✓ Model directory found")

    scorer = FatigueScoringAgent()

    passed = 0
    failed = 0

    results = []

    try:

        # ====================================================
        # TEST ALL FOUR IMAGES
        # ====================================================

        for test_case in TEST_CASES:

            image_name = test_case["name"]
            expected_risk = test_case["expected_risk"]
            expected_score = test_case["expected_score"]

            image_path = IMAGE_DIR / image_name

            print("\n" + "=" * 70)
            print(
                f"Testing: {image_name}"
            )
            print("=" * 70)

            try:

                # ------------------------------------------------
                # 1. IMAGE CHECK
                # ------------------------------------------------

                assert image_path.exists(), (
                    f"Image not found: {image_path}"
                )

                assert image_path.is_file(), (
                    f"Image path is not a file: {image_path}"
                )

                file_size = image_path.stat().st_size

                assert file_size > 0, (
                    f"Image file is empty: {image_path}"
                )

                print(
                    f"\n✓ Image exists "
                    f"({file_size:,} bytes)"
                )

                # ------------------------------------------------
                # 2. IMAGE ANALYSIS
                # ------------------------------------------------

                agent = ImageAnalysisAgent(
                    str(MODEL_DIR)
                )

                try:

                    features = agent.analyze(
                        str(image_path)
                    )

                finally:

                    agent.close()

                print(
                    "✓ Image analysis completed"
                )

                # ------------------------------------------------
                # 3. VALIDATE CV FEATURES
                # ------------------------------------------------

                check_cv_features(
                    features
                )

                print(
                    "✓ CV feature contract valid"
                )

                # ------------------------------------------------
                # SHOW CV FEATURES
                # ------------------------------------------------

                print_cv_features(
                    features
                )

                # ------------------------------------------------
                # 4. FATIGUE SCORING
                # ------------------------------------------------

                result = scorer.score(
                    features
                )

                print(
                    "\n✓ Fatigue scoring completed"
                )

                # ------------------------------------------------
                # 5. VALIDATE RESULT STRUCTURE
                # ------------------------------------------------

                assert isinstance(
                    result,
                    dict
                ), (
                    "Fatigue result must be a dictionary."
                )

                assert "fatigue_score" in result, (
                    "Missing fatigue_score."
                )

                assert "risk_level" in result, (
                    "Missing risk_level."
                )

                assert "components" in result, (
                    "Missing components."
                )

                # ------------------------------------------------
                # 6. VALIDATE SCORE
                # ------------------------------------------------

                check_score_range(
                    result["fatigue_score"]
                )

                # ------------------------------------------------
                # 7. VALIDATE RISK
                # ------------------------------------------------

                check_risk_level(
                    result["risk_level"]
                )

                # ------------------------------------------------
                # 8. VALIDATE COMPONENTS
                # ------------------------------------------------

                check_components(
                    result["components"],
                    result["fatigue_score"]
                )

                # ------------------------------------------------
                # SHOW FATIGUE RESULT
                # ------------------------------------------------

                print_fatigue_result(
                    result
                )

                # ------------------------------------------------
                # SHOW SCORE COMPONENTS
                # ------------------------------------------------

                print_score_components(
                    result["components"]
                )

                # ------------------------------------------------
                # 9. REGRESSION CHECK
                # ------------------------------------------------

                check_expected_result(
                    image_name,
                    result,
                    expected_risk,
                    expected_score
                )

                print(
                    "\n✓ Score range valid"
                )

                print(
                    "✓ Risk level valid"
                )

                print(
                    "✓ Score components valid"
                )

                print(
                    "✓ Expected regression result matched"
                )

                print(
                    "\nSTATUS: PASS ✓"
                )

                passed += 1

                results.append(
                    {
                        "image": image_name,
                        "status": "PASS",
                        "score": result["fatigue_score"],
                        "risk": result["risk_level"],
                    }
                )

            except Exception as error:

                failed += 1

                print(
                    "\nSTATUS: FAIL ✗"
                )

                print(
                    f"ERROR: {error}"
                )

                results.append(
                    {
                        "image": image_name,
                        "status": "FAIL",
                        "score": None,
                        "risk": None,
                    }
                )

        # ====================================================
        # FINAL SUMMARY
        # ====================================================

        print("\n" + "=" * 70)
        print("REGRESSION TEST SUMMARY")
        print("=" * 70)

        for item in results:

            if item["status"] == "PASS":

                print(
                    f"{item['image']:<30}"
                    f"PASS ✓    "
                    f"Score={item['score']:.2f}    "
                    f"Risk={item['risk']}"
                )

            else:

                print(
                    f"{item['image']:<30}"
                    f"FAIL ✗"
                )

        print("\n" + "-" * 70)

        print(
            f"Tests Passed : "
            f"{passed}/{len(TEST_CASES)}"
        )

        print(
            f"Tests Failed : "
            f"{failed}/{len(TEST_CASES)}"
        )

        # ====================================================
        # FINAL STATUS
        # ====================================================

        if failed == 0:

            print("\n" + "=" * 70)
            print("ALL REGRESSION TESTS PASSED ✓")
            print("=" * 70)

            print(
                "\nCV pipeline is stable and ready "
                "for the next integration step."
            )

        else:

            print("\n" + "=" * 70)
            print("REGRESSION TESTS FAILED ✗")
            print("=" * 70)

            print(
                "\nDo NOT continue to Step 33 yet."
            )

            sys.exit(1)

    finally:

        if hasattr(scorer, "close"):
            scorer.close()


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()