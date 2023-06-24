import pinecone
from dotenv import load_dotenv
import os
import json

from tqdm.auto import tqdm


def saveAllToVdb(folderPath: str) -> None:

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
    allMetadata = [i for i in os.listdir(folderPath) if 'json' in i]

    all_transcripts: list = []
    for file in allMetadata:
        filePath = folderPath + file
        videoID = file.rstrip('.json')


        with open(filePath, 'r', encoding='utf-8') as f:
            text = json.load(f)
        

        for elem in text:
            if elem == "audio_text":
                # create data records
                data = {
                    'id': videoID + '_audio',
                    'values': text["audio_embedding"],
                    'metadata': {'text': text[elem],
                                'url': text['url'],
                                'platform': text['platform']}
                }
                all_transcripts.append(data)

            elif elem == "video_text":
                # create data records
                data = {
                    'id': videoID + '_video',
                    'values': text["video_embedding"],
                    'metadata': {'text': text[elem],
                                'url': text['url'],
                                'platform': text['platform']}
                }
                all_transcripts.append(data)

            elif elem == "audio_segments":
                for item in text[elem]:
                    # create data records
                    data = {
                        'id': videoID + '_' + item + '_audio',
                        'values': text[elem][item]["embedding"],
                        'metadata': {'text': text[elem][item]["text"],
                                    'url': text["url"],
                                    'platform': text["platform"],
                                    'start': text[elem][item]["start"],
                                    'end': text[elem][item]["end"]}
                    }
                    all_transcripts.append(data)
            
            elif elem == "video_segments":
                for item in text[elem]:
                    # create data records
                    data = {
                        'id': videoID + '_' + item + '_video',
                        'values': text[elem][item]["embedding"],
                        'metadata': {'text': text[elem][item]["text"],
                                    'url': text["url"],
                                    'platform': text["platform"],
                                    'start': text[elem][item]["time"]}
                    }
                    all_transcripts.append(data)

    # Upload data in batches, as the max number of requests to do in one upsert is 100
    batch_size = 32

    for i in tqdm(range(0, len(all_transcripts), batch_size)):

        i_end = min(i+batch_size, len(all_transcripts))
        batch = all_transcripts[i:i_end]

        # add to pinecone
        index.upsert(vectors=batch)       




if __name__ == '__main__':

    saveAllToVdb(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/")