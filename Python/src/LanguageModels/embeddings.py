from sentence_transformers import SentenceTransformer
import json
import os


def embeddAll(folderPath: str) -> None:
    mpnet = SentenceTransformer('all-mpnet-base-v2')

    for file in os.listdir(folderPath):
        if 'json' in file:
            filePath = folderPath + file

            with open(filePath, 'r', encoding='utf-8') as f:
                text = json.load(f)

            embedding = mpnet.encode(text['audio_text']).tolist()
            text['audio_embedding'] = embedding
            embedding = mpnet.encode(text['video_text']).tolist()
            text['video_embedding'] = embedding

            for item in text["audio_segments"]:
                embedding = mpnet.encode(text["audio_segments"][item]['text']).tolist()
                text["audio_segments"][item]['embedding'] = embedding
            
            for item in text["video_segments"]:
                embedding = mpnet.encode(text["video_segments"][item]['text']).tolist()
                text["video_segments"][item]['embedding'] = embedding

            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump(text, f, ensure_ascii=False, indent=4)
        
            print(f'Finished embedding {file}')


if __name__ == '__main__':
    embeddAll(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/")