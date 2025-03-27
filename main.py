# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from typing import Optional
from tts import TextToSpeechService
import io
import scipy.io.wavfile as wavfile

print ("Starting Server..")
app = FastAPI()
# Initialize the TTS service (only once)
tts_service = TextToSpeechService()
class TextToSpeechRequest(BaseModel):
    text: str
    voice_preset: Optional[str] = "v2/en_speaker_9" # Optional voice preset

@app.post("/synthesize")
async def synthesize_speech(request: TextToSpeechRequest):
    """
    Synthesizes speech from the given text using the TTS service.
    """ 
    try:
        audio_array, sample_rate = tts_service.synthesize(request.text, request.voice_preset)
        wav_buffer = io.BytesIO()
        wavfile.write(wav_buffer, sample_rate, audio_array)
        wav_buffer.seek(0)

        return StreamingResponse(
            wav_buffer,
            media_type="audio/wav",
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error during synthesis: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Performs a health check to verify that the service is running.
    """
    return {"status": "ok"}