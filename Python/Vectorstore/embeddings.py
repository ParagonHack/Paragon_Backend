from sentence_transformers import SentenceTransformer
import json
import os


def embeddAll() -> None:
    mpnet = SentenceTransformer('all-mpnet-base-v2')

    transcripts = os.listdir(f"{os.getcwd()}/Paragon_Backend/Python/Data/transcripts/")

    for file in transcripts:
        filePath = f"{os.getcwd()}/Paragon_Backend/Python/Data/transcripts/" + file

        with open(filePath, 'r', encoding='utf-8') as f:
            text = json.load(f)

        embedding = mpnet.encode(text['text']).tolist()
        text['embedding'] = embedding

        with open(filePath, 'w', encoding='utf-8') as f:
            json.dump(text, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    embeddAll()