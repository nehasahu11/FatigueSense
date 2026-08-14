from pathlib import Path

from backend.app.agents.image_analysis_agent import ImageAnalysisAgent
from backend.app.agents.fatigue_scoring_agent import FatigueScoringAgent


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

MODEL_DIR = "backend/data/models"
IMAGE_DIR = Path("backend/data/test_images")


# Use the four images that currently exist in your project.
TEST_IMAGES = [
    "image_1_rested.png",
    "image_2_mild_fatigue.png",
    "image_3_high_fatigue.png",
    "image_4_edge_case.png",
]


# ---------------------------------------------------------
# Main test function
# ---------------------------------------------------------

def main():

    scorer = FatigueScoringAgent()

    print("\n" + "=" * 70)
    print("FATIGUESENSE - FATIGUE PIPELINE TEST")
    print("=" * 70)

    for image_name in TEST_IMAGES:

        image_path = IMAGE_DIR / image_name

        print("\n" + "-" * 70)
        print(f"Testing: {image_name}")
        print("-" * 70)

        # -------------------------------------------------
        # Check image exists
        # -------------------------------------------------

        if not image_path.exists():
            print(f"ERROR: Image not found: {image_path}")
            continue

        # -------------------------------------------------
        # Create image analysis agent
        # -------------------------------------------------

        agent = ImageAnalysisAgent(MODEL_DIR)

        try:

            # -------------------------------------------------
            # Analyze image
            # -------------------------------------------------

            features = agent.analyze(str(image_path))

        except Exception as e:

            print(f"ERROR during image analysis: {e}")
            continue

        finally:

            # -------------------------------------------------
            # Close MediaPipe/model resources
            # -------------------------------------------------

            if hasattr(agent, "close"):
                agent.close()

        # -------------------------------------------------
        # Calculate fatigue score
        # -------------------------------------------------

        try:

            result = scorer.score(features)

        except Exception as e:

            print(f"ERROR during fatigue scoring: {e}")
            continue

        # -------------------------------------------------
        # Display extracted CV features
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Display fatigue result
        # -------------------------------------------------

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

        # -------------------------------------------------
        # Display individual scoring components
        # -------------------------------------------------

        print("\nSCORE COMPONENTS")
        print("-" * 40)

        components = result.get("components", {})

        print(
            f"Eye Closure     : "
            f"{components.get('eye_closure_score', 0)}"
        )

        print(
            f"Eye State       : "
            f"{components.get('eye_state_score', 0)}"
        )

        print(
            f"Blink           : "
            f"{components.get('blink_score', 0)}"
        )

        print(
            f"Yawn            : "
            f"{components.get('yawn_score', 0)}"
        )

        print(
            f"Dark Circle     : "
            f"{components.get('dark_circle_score', 0)}"
        )

    # ---------------------------------------------------------
    # Testing complete
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("TESTING COMPLETE")
    print("=" * 70)

    # Close scorer if the class provides a close method.
    if hasattr(scorer, "close"):
        scorer.close()


# ---------------------------------------------------------
# Entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()