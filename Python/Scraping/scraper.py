from VideoParsers import YtDownloader, TTDownloader, IGDownloader
import os
import json
import cv2


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
        cv2.imwrite(savePath, image)  # save frame as JPEG file  




### Main
def scrapeAll():
    with open(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/videoURLs.txt") as f: 
        links = [item.strip() for item in f.read().split('\n')]

    linkDict = getLinkDict(links)

    outPath = f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/"

    fileName = 0
    for platform, links in linkDict.items():
        if platform == 'tiktok':
            for url in links:
                # Download the video
                TTDownloader(url, outPath + 'tiktok', str(fileName))

                # Create and save metadata file
                data = {
                        "site": "tiktok",
                        "url": url,
                        "username": "n/a",
                        "username_url": "n/a",
                        "description": "n/a"
                        }
                with open(f'{os.getcwd()}/Paragon_Backend/Python/Data/videos/tiktok/{fileName}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                
                # Get first video frame and save thumbnail as JPEG/PNG
                savePath = outPath + 'tiktok/' + str(fileName) + '.png'
                videoPath = outPath + 'tiktok/' + str(fileName) + '.mp4'
                getFirstFrame(videoPath, savePath)

                # Iterate fileID by 1 for the next file
                fileName += 1
        
        elif platform == 'instagram':
            for url in links:
                # Download the video
                IGDownloader(url, outPath + 'instagram', str(fileName))

                # Create and save metadata file
                data = {
                        "site": "instagram",
                        "url": url,
                        "username": "n/a",
                        "username_url": "n/a",
                        "description": "n/a"
                        }
                with open(f'{os.getcwd()}/Paragon_Backend/Python/Data/videos/instagram/{fileName}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                
                # Get first video frame and save thumbnail as JPEG/PNG
                savePath = outPath + 'instagram/' + str(fileName) + '.png'
                videoPath = outPath + 'instagram/' + str(fileName) + '.mp4'
                getFirstFrame(videoPath, savePath)


                # Iterate fileID by 1 for the next file
                fileName += 1
        
        elif platform == 'youtube':
            for url in links:
                # Download the video
                YtDownloader(url, outPath + 'youtube', str(fileName))

                # Create and save metadata file
                data = {
                        "site": "youtube",
                        "url": url,
                        "username": "n/a",
                        "username_url": "n/a",
                        "description": "n/a"
                        }
                with open(f'{os.getcwd()}/Paragon_Backend/Python/Data/videos/youtube/{fileName}.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                
                # Get first video frame and save thumbnail as JPEG/PNG
                savePath = outPath + 'youtube/' + str(fileName) + '.png'
                videoPath = outPath + 'youtube/' + str(fileName) + '.mp4'
                getFirstFrame(videoPath, savePath)

                # Iterate fileID by 1 for the next file
                fileName += 1





if __name__ == '__main__':
    scrapeAll()