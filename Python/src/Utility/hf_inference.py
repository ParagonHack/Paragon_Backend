import json, os, base64
from typing import List
from PIL import Image
import requests
from dotenv import load_dotenv


def transcribe_image(endpoint: str, pathImage: str) -> str:

    load_dotenv(f"{os.getcwd()}/.env")
    HF_TOKEN = os.environ.get("HuggingFace_Key")

    ENDPOINT_URL = endpoint

    with open(pathImage, "rb") as f:
        data = f.read()
    
    req = {"inputs": base64.b64encode(data).decode('utf-8')}
    response = requests.request("POST", ENDPOINT_URL, headers={"Authorization": f"Bearer {HF_TOKEN}"}, json=req)
    
    return json.loads(response.content.decode("utf-8"))['captions']



if __name__ == '__main__':
    transcribe_image(endpoint= None, pathImage= f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/0.json")
