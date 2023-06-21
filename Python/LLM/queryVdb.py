from sentence_transformers import SentenceTransformer
import pinecone

from dotenv import load_dotenv
import os
import json

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


mpnet = SentenceTransformer('all-mpnet-base-v2')

query = 'Berlin'

query_emb = mpnet.encode(query).tolist()

output = index.query(query_emb, top_k=4, include_metadata=True)

print(output)



# for context in output['matches']:
#     print(context['metadata']['text'], end="\n---\n")