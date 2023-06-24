from src.Scraping.scraper import scrapeAll

from src.LanguageModels.transcriber import transcribeAudioAll, transcribeVideoAll
from src.LanguageModels.embeddings import embeddAll

from src.Databases.pinecone_vdb import saveAllToVdb
from src.Databases.aws_s3_db import saveAllToS3


import os

folderPath = f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/"
HF_Endpoint = ""


# # Scrape the videos from all links from Data/videos/videosURLs.txt
print('Scraping Videos..')
scrapeAll(folderPath)
print('Finished scraping!')


# Transcribe all mp4 files 
print('Transcribing audio to text..')
transcribeAudioAll(folderPath)
print('Finished transcribing audio to text!')

print('Transcribing video to text..')
transcribeVideoAll(folderPath, hf_endpoint= HF_Endpoint)
print('Finished transcribing video to text!')

# # Embedd all transcriptions using MpNET
print("Embedding text files..")
embeddAll(folderPath)
print('Finished embedding text!')


# # Save all transcribed files to Pinecone
print('Saving embeddings to Pinecone..')
saveAllToVdb(folderPath)
print('Finished saving the embeddings to the vector database!')


# # Save mp4 + JSON files to S3 for front-end
s3_subFolderName = 'dev_be_1'
print('Saving files to S3..')
saveAllToS3(folderPath, s3_subFolderName, delete=False)
print('Finished saving files to the database!')