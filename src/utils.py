import hashlib
from datetime import datetime
from pathlib import Path
import shutil


def save_file(uploaded_file, root_dir: Path) -> Path:
    """Create a unique folder based on file hash and timestamp"""
    # Create hash of file content
    file_hash = hashlib.md5(uploaded_file.getvalue()).hexdigest()[:8]

    # Create timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create unique folder name
    folder_name = f"{timestamp}_{file_hash}"
    unique_folder = root_dir / "uploads" / folder_name

    # Create folders if they don't exist
    unique_folder.mkdir(parents=True, exist_ok=True)
    (unique_folder / "raw").mkdir(exist_ok=True)
    (unique_folder / "processed").mkdir(exist_ok=True)

    # Save the uploaded file to the "raw" directory
    with open(unique_folder / "raw" / uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return unique_folder
