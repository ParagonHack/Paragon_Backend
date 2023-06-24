###### YOUTUBE  ######
from pytube import YouTube


class YtDownloader():
    def __init__(self, webURL: list, outPath: str, fileName: str):
        self.outPath = outPath
        self.fileName = fileName
        self.url = webURL

        self.YT_download()


    def YT_download(self) -> None:
        self.video = YouTube(self.url, use_oauth=True, allow_oauth_cache=True)

        obj = self.video.streams.filter(file_extension='mp4').first()
        video = self.video.streams.get_by_itag(obj.itag)

        # finally download the YouTube Video...
        video.download(output_path=self.outPath, filename=self.fileName + '.mp4')


        # for streams in obj:
        #     # print itag, resolution and codec format of Mp4 streams
        #     print(f"Video itag : {streams.itag} Resolution : {streams.resolution} VCodec : {streams.codecs[0]}")

        # # enter the itag value of resolution on which you want to download the video
        # input_itag = input("Enter itag Value : ")
        # get video using itag vale


###### TIKTOK  ######
import requests


class TTDownloader():
    def __init__(self, webURL: str, outPath: str, fileName:str):
        self.outPath = outPath
        self.fileName = fileName
        self.url = webURL

        self.TT_download()



    def getDict(self) -> dict:
        response = requests.get('https://ttdownloader.com/')
        point = response.text.find('<input type="hidden" id="token" name="token" value="') + \
            len('<input type="hidden" id="token" name="token" value="')
        token = response.text[point:point+64]
        TTDict = {
            'token': token,
        }

        for i in response.cookies:
            TTDict[str(i).split()[1].split('=')[0].strip()] = str(
                i).split()[1].split('=')[1].strip()
        return TTDict

    def createHeader(self, parseDict) -> list:

        cookies = {
            'PHPSESSID': parseDict['PHPSESSID'],
            # 'popCookie': parseDict['popCookie'],
        }
        headers = {
            'authority': 'ttdownloader.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://ttdownloader.com',
            'referer': 'https://ttdownloader.com/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        data = {
            'url': '',
            'format': '',
            'token': parseDict['token'],
        }
        return cookies, headers, data


    def TT_download(self) -> None:
        parseDict = self.getDict()
        cookies, headers, data = self.createHeader(parseDict)

        data['url'] = self.url

        response = requests.post('https://ttdownloader.com/search/',
                                cookies=cookies, headers=headers, data=data)
        try:
            linkParse = [i for i in str(response.text).split()
                        if i.startswith("href=")][0]

            response = requests.get(linkParse[6:-10])
            with open(self.outPath + '/' + self.fileName + ".mp4", "wb") as f:
                f.write(response.content)
        except IndexError:
            return


###### INSTAGRAM  ######
import instaloader


class IGDownloader():
    def __init__(self, webURL: str, outPath: str, fileName:str):
        self.outPath = outPath
        self.fileName = fileName
        self.url = webURL

        self.IG_download()
    
    def IG_download(self) -> None:
        obj = instaloader.Instaloader()
        try:
            post = instaloader.Post.from_shortcode(obj.context, self.url.split('p/')[1].strip('/ '))
        except IndexError:
            post = instaloader.Post.from_shortcode(obj.context, self.url.split('reel/')[1].strip('/ '))

        photo_url = post.url
        video_url = post.video_url
        if video_url:
            response = requests.get(video_url)
            with open(self.outPath + '/' +  self.fileName + ".mp4", "wb") as f:
                f.write(response.content)
        elif photo_url:
            response = requests.get(photo_url)
            with open(self.outPath + '/' +  self.fileName + ".jpg", "wb") as f:
                f.write(response.content)
