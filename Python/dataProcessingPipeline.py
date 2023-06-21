from Scraping.scraper import scrapeAll
from STT.transcriber import transcribeAll
from Vectorstore.embeddings import embeddAll
from Vectorstore.pinecone_vdb import saveAllToVdb


# Scrape the videos from all links from Data/videos/videosURLs.txt
scrapeAll()

# Transcribe all mp4 files 
transcribeAll()

# Embedd all transcriptions using MpNET
embeddAll()

# Save all transcribed files to Pinecone
saveAllToVdb()