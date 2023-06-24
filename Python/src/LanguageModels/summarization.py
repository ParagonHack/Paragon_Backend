from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

from dotenv import load_dotenv
import os




def summarizeDescriptionList(descriptionList: list) -> str:

    load_dotenv(f"{os.getcwd()}/.env")
    OAI_key = os.environ.get("OpenAI_Key")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap  = 20)

    docs = text_splitter.create_documents(['New Frame: ' + '\n New Frame: '.join(descriptionList)])

    llm = OpenAI(temperature=0.8, openai_api_key=OAI_key)

    chain = load_summarize_chain(llm, chain_type="stuff")

    return chain.run(docs)


