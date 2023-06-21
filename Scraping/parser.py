from VideoParsers import YtDownloader, TTDownloader, IGDownloader

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


def main(linkDict):
    outPath = './data/videos/'
    fileName = '0'


    YtDownloader(linkDict['youtube'], outPath + 'youtube', fileName)

    TTDownloader(linkDict['tiktok'], outPath + 'tiktok', fileName)

    IGDownloader(linkDict['instagram'], outPath + 'instagram', fileName)


if __name__ == '__main__':
    with open("./data/videos/dataLinks.txt") as f: 
        links = [item.strip() for item in f.read().split('\n')]

    linkDict = getLinkDict(links)

    main(linkDict)