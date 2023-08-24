import os
from random import choice
from string import ascii_lowercase, ascii_uppercase, digits
from pathlib import Path
from werkzeug.utils import secure_filename

from ..config import UPLOADS_DIR

CHARS = ascii_uppercase + ascii_lowercase + digits

def secure_unique_filename_for_directory(filename: str, directory: Path=UPLOADS_DIR, n: int=6) -> Path:
    if not directory.is_dir():
        raise OSError("`directory` is not a directory!")

    filename = secure_filename(filename)
    stub, ext = os.path.splitext(filename)

    while Path(directory / filename).exists():
        filename = secure_filename(f"{stub}{''.join([choice(CHARS) for _ in range(n)])}{ext}")
    return filename





