# import os
# import whisper


# model = whisper.load_model('large')

# text = model.transcribe('./vids/tiktok5.mp4')

# print(text)

import openai
from dotenv import load_dotenv
import os

load_dotenv(f"{os.getcwd()}/.env")

openai.api_key = os.environ.get("OpenAI_Key")

file = open("./vids/tiktok3.mp4", "rb")
transcription = openai.Audio.transcribe("whisper-1", file)

print(transcription)