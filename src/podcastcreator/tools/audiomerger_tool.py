from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from pydub import AudioSegment
import os

class MergeAudioInput(BaseModel):
    """Input schema for MergeAudioTool."""

class MergeAudioTool(BaseTool):
    name: str = "Audio Merger"
    description: str = "A tool that merges multiple WAV files into a single WAV file using pydub."

    args_schema: Type[BaseModel] = MergeAudioInput

    def _run(self) -> str:
        # Get a list of all WAV files in the folder
        folder_path = "Data"
        output_file = "podcast.wav"
        wav_files = [f for f in os.listdir(folder_path) if f.endswith(".wav")]

        # Sort the files alphabetically to ensure consistent merging order
        wav_files.sort()

        # Initialize an empty AudioSegment
        merged_audio = AudioSegment.empty()

        # Iterate through the WAV files and append them to the merged_audio
        for wav_file in wav_files:
            file_path = os.path.join(folder_path, wav_file)
            audio = AudioSegment.from_wav(file_path)
            merged_audio += audio

        # Export the merged audio
        output_path = os.path.join(folder_path, output_file)
        merged_audio.export(output_path, format="wav")

        return f"Merged {len(wav_files)} WAV files into {output_path}"