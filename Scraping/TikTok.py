import requests
# import instaloader



def getList()->list:
    with open("./data/data.txt") as f: return [item.strip() for item in f.read().split('\n')]

def getLinkDict()->dict:
    values={"tiktok":[],"instagram":[]}
    for item in getList():
        if item.startswith('https://www.instagram.com'):
            values['instagram'].append(item)
        elif item.startswith('https://www.tiktok.com') or item.startswith('https://m.tiktok.com'):
            values['tiktok'].append(item)
    return values

def getDict() -> dict:
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

def createHeader(parseDict) -> list:

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


def TDL(cookies, headers, data, name) -> None:
    response = requests.post('https://ttdownloader.com/search/',
                             cookies=cookies, headers=headers, data=data)
    linkParse = [i for i in str(response.text).split()
                 if i.startswith("href=")][0]

    response = requests.get(linkParse[6:-10])
    with open("./vids/"+"tiktok"+name+".mp4", "wb") as f:
        f.write(response.content)


def TDLALL() -> None:
    parseDict = getDict()
    cookies, headers, data = createHeader(parseDict)
    linkList = getLinkDict()['tiktok']
    for i in linkList:
        try:
            data['url'] = i
            TDL(cookies, headers, data, str(linkList.index(i)))
        except IndexError:
            parseDict = getDict()
            cookies, headers, data = createHeader(parseDict)
        except Exception as err:
            print(err)
            exit(1)


if __name__ == "__main__":
    TDLALL()
    # IDLALL()
    pass