from Scraping.VideoParsers import YtDownloader, TTDownloader, IGDownloader
import os, json, cv2
import pandas as pd


### Functions

def getLinkDict(linkList: list) -> dict:
    values={"tiktok":[],"instagram":[], "youtube": []}
    for item in linkList:
        if item.startswith('https://www.instagram.com'):
            values['instagram'].append(item)
        elif item.startswith('https://www.tiktok.com') or item.startswith('https://m.tiktok.com'):
            values['tiktok'].append(item)
        elif item.startswith('https://www.youtube.com'):
            values['youtube'].append(item)
    return values



def getFirstFrame(videoPath, savePath):
    vidcap = cv2.VideoCapture(videoPath)
    success, image = vidcap.read()
    if success:
        cv2.imwrite(savePath, image)  # save frame as PNG file  




### Main
def scrapeAll(outPath: str):
    print(os.getcwd())
    with open(outPath + "videosURLs.txt") as f: 
        links = [item.strip() for item in f.read().split('\n')]

    linkDict = getLinkDict(links)


    fileName = 0
    for platform, links in linkDict.items():
        for url in links:
            if len(str(fileName)) == 1:
                strFileName = '0'+fileName
            else:
                strFileName = str(fileName)

            # Download the video
            if platform == 'tiktok': 
                TTDownloader(url, outPath, strFileName)
                metadata = pd.read_csv(outPath + 'TT_metadata.csv')
            elif platform == 'instagram': 
                IGDownloader(url, outPath, strFileName)
            if platform == 'youtube': 
                YtDownloader(url, outPath, strFileName)
                metadata = pd.read_csv(outPath + 'Yt_metadata.csv')
                user = metadata[metadata['Link'] == "https://www.youtube.com/watch?v=q8DpEhLMLYI&pp=ygUGdHJhdmVs"]['Channel Name']._values[0]
                user_link = metadata[metadata['Link'] == "https://www.youtube.com/watch?v=q8DpEhLMLYI&pp=ygUGdHJhdmVs"]['Channel Link']._values[0]
                description = metadata[metadata['Link'] == "https://www.youtube.com/watch?v=q8DpEhLMLYI&pp=ygUGdHJhdmVs"]['Description']._values[0]

            # Get the video's metadata
            

            # Create and save metadata file
            data = {
                    "platform": platform,
                    "url": url,
                    "username": user,
                    "username_url": user_link,
                    "description": "n/a"
                    }
            
            with open(outPath + f'{strFileName}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            # Get first video frame and save thumbnail as JPEG/PNG
            savePath = outPath + strFileName + '.png'
            videoPath = outPath + strFileName + '.mp4'
            getFirstFrame(videoPath, savePath)

            # Iterate fileID by 1 for the next file
            fileName += 1



if __name__ == '__main__':
    scrapeAll("./Data/videos/")