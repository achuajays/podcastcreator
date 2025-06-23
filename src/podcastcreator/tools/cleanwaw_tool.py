from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import os

class CleanWavFilesInput(BaseModel):
    """Input schema for CleanWavFilesTool."""

class CleanWavFilesTool(BaseTool):
    name: str = "WAV Files Cleaner"
    description: str = "A tool that deletes all WAV files in a folder except for a specified file."

    args_schema: Type[BaseModel] = CleanWavFilesInput

    def _run(self) -> str:
        # Get a list of all files in the folder
        folder_path = os.getenv("Folder")
        keep_file = "podcast.wav"
        all_files = os.listdir(folder_path)

        # Iterate through the files and delete .wav files except the one to keep
        deleted_files = []
        for file_name in all_files:
            if file_name.endswith(".wav") and file_name != keep_file:
                file_path = os.path.join(folder_path, file_name)
                try:
                    os.remove(file_path)
                    deleted_files.append(file_name)
                except OSError as e:
                    return f"Error deleting {file_name}: {e}"

        return f"Deleted {len(deleted_files)} WAV files. Kept: {keep_file}"
