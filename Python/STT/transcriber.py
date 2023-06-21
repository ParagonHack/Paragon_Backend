from Whisper import transcribe_audio
import os
import json

def getItem(item: str, platform: int) -> None:
    outPath = f"{os.getcwd()}/Paragon_Backend/Python/Data/transcripts/"

    if platform == 0:
        platform = 'instagram'
    elif platform == 1:
        platform = 'youtube'
    elif platform == 2:
        platform = 'tiktok'

    videoPath = f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/{platform}/" + item

    transcript = transcribe_audio(videoPath)

    with open(outPath + item[:item.find('.mp4')] + ".json", 'w', encoding='utf-8') as f:
        json.dump(transcript, f, ensure_ascii=False, indent=4)



def transcribeAll() -> None:

    insta_files = os.listdir(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/instagram")
    yt_files = os.listdir(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/youtube")
    tiktok_files = os.listdir(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/tiktok")

    files = [insta_files, yt_files, tiktok_files]

    for platform in files:
        for item in platform:
            if 'mp4' in item:
                getItem(item, files.index(platform))


if __name__ == '__main__':
    transcribeAll()