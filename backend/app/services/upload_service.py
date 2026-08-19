import os
import uuid
from pathlib import Path


class UploadService:

    ALLOWED_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".webp"
    }

    def __init__(self):

        self.upload_dir = Path(
            os.getenv(
                "UPLOAD_DIR",
                "data/uploads"
            )
        )

        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def save_file(
        self,
        file
    ):

        original_name = file.filename

        extension = (
            Path(original_name)
            .suffix
            .lower()
        )

        if extension not in self.ALLOWED_EXTENSIONS:

            raise ValueError(
                "Unsupported image format"
            )

        unique_name = (
            f"{uuid.uuid4()}"
            f"{extension}"
        )

        file_path = (
            self.upload_dir
            / unique_name
        )

        with open(
            file_path,
            "wb"
        ) as output:

            output.write(
                file.file.read()
            )

        return str(file_path)