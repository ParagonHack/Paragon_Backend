import pinecone
from dotenv import load_dotenv
import os
import json


def saveAllToVdb() -> None:

    load_dotenv(f"{os.getcwd()}/.env")

    # connect to pinecone (get API key and env at app.pinecone.io)
    pinecone.init(api_key=os.environ.get("Pinecone_Key"), environment=os.environ.get("Pinecone_Environ"))

    try:
        # create index
        pinecone.create_index(
            'social-media-search',
            dimension=768, metric='cosine'
        )
    except:
        print('Index already exists! Importing...')

    # connect to the index
    index = pinecone.Index('social-media-search')


    # import embeddings
    transcripts = os.listdir(f"{os.getcwd()}/Paragon_Backend/Python/Data/transcripts/")

    all_transcripts: list = []
    for file in transcripts:
        filePath = f"{os.getcwd()}/Paragon_Backend/Python/Data/transcripts/" + file
        videoID = file.rstrip('.json')
        with open(filePath, 'r', encoding='utf-8') as f:
            text = json.load(f)
        
        # create metadata records
        data = {
            'id': videoID,
            'values': text['embedding'],
            'metadata': {'text': text['text']}
        } 

        all_transcripts.append(data)

    # add to pinecone
    index.upsert(vectors=all_transcripts)       

if __name__ == '__main__':
    saveAllToVdb()