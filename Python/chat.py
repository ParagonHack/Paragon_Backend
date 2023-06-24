# from LLM.OpenAI import loadOAI
# from LLM.queryVdb import queryVdb
# from LLM.promptTemplates import mainChatPrompt

import streamlit as st
import pinecone
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv
import os


    

@st.experimental_singleton
def init_pinecone():
    load_dotenv(f"{os.getcwd()}/.env")
    # connect to pinecone (get API key and env at app.pinecone.io)
    pinecone.init(api_key=os.environ.get("Pinecone_Key"), environment=os.environ.get("Pinecone_Environ"))

    return pinecone.Index('social-media-search')
    
@st.experimental_singleton
def init_retriever():
    return SentenceTransformer('all-mpnet-base-v2')

index = init_pinecone()
retriever = init_retriever()

def card(thubmnail, url, context):
    return st.markdown(f"""
    <div class="container-fluid">
        <div class="row align-items-start">
            <div class="col-md-4 col-sm-4">
                 <div class="position-relative">
                     <a href={url}><img src={thubmnail} class="img-fluid" style="width: 192px; height: 106px"></a>
                 </div>
             </div>
             <div  class="col-md-8 col-sm-8">
                 <a href={url}</a>
                 <br>
                 <span style="color: #808080;">
                     <small>{context[:200].capitalize()+"...."}</small>
                 </span>
             </div>
        </div>
     </div>
        """, unsafe_allow_html=True)

    
st.write("""
# Social Media Gatherer
Ask me a question!
""")

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
""", unsafe_allow_html=True)

query = st.text_input("Search!", "")

if query != "":
    xq = retriever.encode([query]).tolist()
    xc = index.query(xq, top_k=5, include_metadata=True)
    
    for context in xc['matches']:
        print(context['metadata']['local_url'].replace('.mp4', '.png'))
        card(
            context['metadata']['local_url'].replace('.mp4', '.png'),
            context['metadata']['local_url'],
            context['metadata']['text']
        )