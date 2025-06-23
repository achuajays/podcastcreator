from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List
from sarvamai import SarvamAI
from sarvamai.play import save
import os

class TextToSpeechInput(BaseModel):
    """Input schema for TextToSpeechTool."""
    texts: List[str] = Field(..., description="List of texts to convert to speech.")

class TextToSpeechTool(BaseTool):
    name: str = "Text to Speech Converter"
    description: str = "A tool that converts a list of texts to speech using the SarvamAI API."

    args_schema: Type[BaseModel] = TextToSpeechInput

  
    def _run(self, texts: List[str]) -> str:
        results = []
        api_key = os.getenv("SARVAM_API_KEY")
        client = SarvamAI(api_subscription_key=api_key)
        for j, text in enumerate(texts):
            audio = client.text_to_speech.convert(
                target_language_code="en-IN",
                text=text,
                model="bulbul:v2",
                speaker="anushka"
            )
            output_file = f"Data/output{j}.wav"
            save(audio, output_file)
            results.append(f"Speech saved to {output_file}")
        return "\n".join(results)
