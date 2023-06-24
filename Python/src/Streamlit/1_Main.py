import os
import streamlit as st
from streamlit_chat import message

from sentence_transformers import SentenceTransformer
import pinecone

from dotenv import load_dotenv
import os



def queryVdb(query):
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


    query_emb = mpnet.encode(query).tolist()

    output = index.query(query_emb, top_k=4, include_metadata=True)

    return output

st.set_page_config(page_title="Social Media Searc", page_icon=":robot:")
st.header("Search through a database of social media videos")


if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

# st.video(data, format="video/mp4", start_time=0)

user_input=st.text_input("You:",key='input')
if user_input:
    output = queryVdb(user_input)
    #store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)


if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i]['matches'][0]['id'], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

video_file = open('myvideo.mp4', 'rb')
video_bytes = video_file.read()

st.video(video_bytes)