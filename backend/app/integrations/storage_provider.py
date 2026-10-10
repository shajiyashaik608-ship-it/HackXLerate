import os
import uuid
import aiofiles
from pathlib import Path
from typing import Tuple
from app.core.config import settings
from app.core.exceptions import ValidationException


# File signature magic bytes
MAGIC_NUMBERS = {
    "pdf": b"%PDF",
    "png": b"\x89PNG\r\n\x1a\n",
    "jpg": b"\xff\xd8\xff",
    "jpeg": b"\xff\xd8\xff",
}


class StorageProvider:
    """Manages secure, private local storage for patient medical documents."""

    def __init__(self, base_dir: str = settings.UPLOAD_DIR):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def validate_file_content(self, filename: str, content: bytes) -> str:
        """
        Validate file size and verify true binary signature (magic bytes).
        Returns normalized file extension ('pdf', 'png', 'jpg').
        """
        if not content or len(content) == 0:
            raise ValidationException("The uploaded file is empty.")

        if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
            max_mb = settings.MAX_UPLOAD_SIZE_BYTES / (1024 * 1024)
            raise ValidationException(f"File size exceeds maximum permitted limit of {max_mb:.0f} MB.")

        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext not in ["pdf", "png", "jpg", "jpeg"]:
            raise ValidationException(f"Unsupported file extension '.{ext}'. Supported formats: PDF, PNG, JPG/JPEG.")

        # Validate magic bytes
        if ext == "pdf":
            if not content.startswith(b"%PDF"):
                raise ValidationException("Invalid or corrupt PDF document header.")
            return "pdf"
        elif ext == "png":
            if not content.startswith(b"\x89PNG"):
                raise ValidationException("Invalid or corrupt PNG image signature.")
            return "png"
        elif ext in ["jpg", "jpeg"]:
            if not content.startswith(b"\xff\xd8\xff"):
                raise ValidationException("Invalid or corrupt JPEG/JPG image signature.")
            return "jpg"

        raise ValidationException("File format signature validation failed.")

    async def save_file(self, user_id: int, original_filename: str, content: bytes) -> Tuple[str, str]:
        """
        Saves document inside user-specific isolated private folder.
        Returns: (relative_file_path, normalized_file_type)
        """
        file_type = self.validate_file_content(original_filename, content)
        user_folder = self.base_dir / f"user_{user_id}"
        user_folder.mkdir(parents=True, exist_ok=True)

        unique_id = uuid.uuid4().hex
        safe_filename = f"{unique_id}.{file_type}"
        file_path = user_folder / safe_filename

        async with aiofiles.open(file_path, "wb") as f:
            await f.write(content)

        return str(file_path), file_type

    def read_file(self, file_path_str: str) -> bytes:
        """Reads file bytes from private storage."""
        file_path = Path(file_path_str)
        if not file_path.exists():
            raise ValidationException("Stored medical document was not found.")
        return file_path.read_bytes()

    def delete_file(self, file_path_str: str) -> bool:
        """Deletes file from private storage."""
        file_path = Path(file_path_str)
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def purge_user_files(self, user_id: int) -> int:
        """Removes all stored private files for a user."""
        user_folder = self.base_dir / f"user_{user_id}"
        deleted_count = 0
        if user_folder.exists() and user_folder.is_dir():
            for item in user_folder.iterdir():
                if item.is_file():
                    item.unlink()
                    deleted_count += 1
            try:
                user_folder.rmdir()
            except OSError:
                pass
        return deleted_count


storage_provider = StorageProvider()
