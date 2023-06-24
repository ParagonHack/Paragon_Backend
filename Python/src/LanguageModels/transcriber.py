from LanguageModels.speechToText import transcribe_audio
from LanguageModels.imageToText import local_transcribe_image, inference_transcribe_image
from LanguageModels.summarization import summarizeDescriptionList

from transformers import BlipForConditionalGeneration, BlipProcessor
from PIL import Image

import os
import json
import cv2
    

def transcribeAudioAll(path: str) -> None:
    for item in os.listdir(path):
        if 'mp4' in item:
            videoPath = path + item
            dataPath = path + item[:item.find('.mp4')] + ".json"

            with open(dataPath, 'r+', encoding='utf-8') as f:
                data = json.load(f)

            output: dict = {}

            raw_transcript = transcribe_audio(videoPath)

            output['video_id'] = item[:item.find('.mp4')]
            output['audio_text'] = raw_transcript['text']

            allSegments: dict = {}
            segmentsList = [dict(i) for i in raw_transcript['segments']]
            for segment in segmentsList:
                allSegments[segment['id']] = {
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text']
                }

            output['audio_segments'] = allSegments

            newData = data.copy()
            newData.update(output)

            with open(dataPath, 'w', encoding='utf-8') as f:
                json.dump(newData, f, ensure_ascii=False, indent=4)


def transcribeVideoAll(path: str, hf_endpoint: str) -> None:
    
    for item in os.listdir(path):
        if 'mp4' in item:
            videoPath = path + item

            def getFrame(vid, sec):
                vid.set(cv2.CAP_PROP_POS_MSEC, sec*1000)
                hasFrames,image = vid.read()
                if hasFrames:
                    cv2.imwrite(videoPath.replace('.mp4', '') + '_' +str(sec)+"sec.png", image)     # save frame as PNG file
                return hasFrames

            sec = 0
            frameRate = 3 #it will capture image in each 1 second

            vidcap = cv2.VideoCapture(videoPath)
            descriptionList: list = []

            
            # Get first frame
            success = getFrame(vidcap,sec)
            answer = inference_transcribe_image(videoPath.replace('.mp4', '') + '_' +str(sec)+"sec.png")
            os.remove(videoPath.replace('.mp4', '') + '_' +str(sec)+"sec.png")
            descriptionList.append(answer)

            allSegments: dict = {}
            _id = 0
            allSegments[_id] = {
                'time': sec,
                'text': answer
            }

            # If the first frame was found successfully, loop through the other frames with frameRate as a step
            while success:
                sec = sec + frameRate
                sec = round(sec, 2)

                frames = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
                fps = vidcap.get(cv2.CAP_PROP_FPS)

                seconds = round(frames / fps)
                success = getFrame(vidcap, sec)

                if seconds > sec:
                    
                    answer = inference_transcribe_image(videoPath.replace('.mp4', '') + '_' +str(sec)+"sec.png")
                    os.remove(videoPath.replace('.mp4', '') + '_' +str(sec)+"sec.png")
                    descriptionList.append(answer)

                    _id += 1
                    allSegments[_id] = {
                                    'time': sec,
                                    'text': answer
                                }
                    
                else:
                    success = False

            videoSummary = summarizeDescriptionList(descriptionList)

            dataPath = path + item[:item.find('.mp4')] + ".json"

            with open(dataPath, 'r+', encoding='utf-8') as f:
                data = json.load(f)
            
            output: dict = {}
            
            output['video_text'] = videoSummary
            output['video_segments'] = allSegments

            newData = data.copy()
            newData.update(output)

            with open(dataPath, 'w', encoding='utf-8') as f:
                json.dump(newData, f, ensure_ascii=False, indent=4)
            
            print(f'Saved video  {item}')


if __name__ == '__main__':
    transcribeAudioAll(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/", hf_endpoint="")