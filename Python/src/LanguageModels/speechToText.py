import openai
from dotenv import load_dotenv
import os

from moviepy.editor import *


def transcribe_audio(filePath):

    load_dotenv(f"{os.getcwd()}/.env")

    openai.api_key = os.environ.get("OpenAI_Key")

    video = VideoFileClip(filePath)

    newName = filePath[:filePath.find('.mp4')] + ".mp3"

    video.audio.write_audiofile(newName)

    file = open(newName, "rb")
    transcription = openai.Audio.transcribe("whisper-1", file, response_format='verbose_json')
    
    return transcription
