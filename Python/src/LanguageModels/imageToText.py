import openai, os, requests, json, torch, base64
from dotenv import load_dotenv
from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor
from typing import List

import torch


def local_transcribe_image(filePath: str):
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

    image = Image.open(filePath).convert('RGB') 

    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)

    return processor.decode(out[0], skip_special_tokens=True)



def inference_transcribe_image(endpoint: str, pathImage: str) -> str:

    load_dotenv(f"{os.getcwd()}/.env")
    HF_TOKEN = os.environ.get("HuggingFace_Key")

    ENDPOINT_URL = endpoint

    with open(pathImage, "rb") as f:
        data = f.read()
    
    req = {"inputs": base64.b64encode(data).decode('utf-8')}
    response = requests.request("POST", ENDPOINT_URL, headers={"Authorization": f"Bearer {HF_TOKEN}"}, json=req)
    
    return json.loads(response.content.decode("utf-8"))['captions']



if __name__ == '__main__':
    print(local_transcribe_image("/Users/elefteriubogdan/Desktop/Pinecone-Hackathon/Paragon_Backend/Python/Data/videos/10.png"))
