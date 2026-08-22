from pathlib import Path

import cv2
import numpy as np
from PIL import Image


DEFAULT_IMAGE_SIZE = 640


def preprocess_image(
    image_path: str,
    target_size: int = DEFAULT_IMAGE_SIZE
) -> np.ndarray:
    """
    Prepare an image for OpenCV/MediaPipe processing.

    The image is:
        1. Loaded using Pillow
        2. Converted to RGB
        3. Resized while preserving aspect ratio
        4. Converted to a NumPy array
        5. Converted from RGB to BGR for OpenCV

    Args:
        image_path: Path to the image.
        target_size: Maximum width or height of the image.

    Returns:
        Preprocessed image as an OpenCV BGR NumPy array.

    Raises:
        FileNotFoundError: If the image does not exist.
        ValueError: If target_size is invalid.
    """

    # ---------------------------------------------------------
    # 1. Validate target size
    # ---------------------------------------------------------

    if target_size <= 0:
        raise ValueError("target_size must be greater than 0.")

    # ---------------------------------------------------------
    # 2. Check that the image exists
    # ---------------------------------------------------------

    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Image file not found: {image_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a file: {image_path}"
        )

    # ---------------------------------------------------------
    # 3. Open image using Pillow
    # ---------------------------------------------------------

    with Image.open(path) as image:

        # -----------------------------------------------------
        # 4. Convert image to RGB
        # -----------------------------------------------------

        image = image.convert("RGB")

        # -----------------------------------------------------
        # 5. Resize while maintaining aspect ratio
        # -----------------------------------------------------

        width, height = image.size

        scale = min(
            target_size / width,
            target_size / height,
            1.0
        )

        new_width = int(width * scale)
        new_height = int(height * scale)

        if scale < 1.0:
            image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

        # -----------------------------------------------------
        # 6. Convert PIL image → NumPy RGB array
        # -----------------------------------------------------

        rgb_array = np.array(image)

    # ---------------------------------------------------------
    # 7. Convert RGB → BGR for OpenCV
    # ---------------------------------------------------------

    bgr_array = cv2.cvtColor(
        rgb_array,
        cv2.COLOR_RGB2BGR
    )

    return bgr_array