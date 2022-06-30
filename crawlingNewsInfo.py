from bs4 import BeautifulSoup
import requests
import re

from tqdm import tqdm

metaData = {
    "date":
    [
        {
            "type": "property",
            "value": "published_time"
        },
        {
            "type": "name",
            "value": "published_time"
        }
    ],
    "publisher":
    [
        {
            "type": "property",
            "value": "site"
        },
        {
            "type": "name",
            "value": "site"
        },
        {
            "type": "property",
            "value": "publisher"
        },
        {
            "type": "name",
            "value": "subject"
        },
        {
            "type": "name",
            "value": "Copyright"
        },
        {
            "type": "name",
            "value": "copyright"
        },
        {
            "type": "property",
            "value": "Copyright"
        },
        {
            "type": "property",
            "value": "copyright"
        }
    ],
    "author":
    [
        {
            "type": "property",
            "value": "author"
        },
        {
            "type": "name",
            "value": "author"
        }
    ],
    "summary":
    [
        {
            "type": "property",
            "value": "description"
        },
        {
            "type": "name",
            "value": "description"
        }
    ],
    "title":
    [
        {
            "type": "property",
            "value": "title"
        },
        {
            "type": "name",
            "value": "title"
        }
    ],
    "link":
    [
        {
            "type": "property",
            "value": "url"
        },
        {
            "type": "name",
            "value": "url"
        }
    ]
}

def getNewsInfo(news_url):
    urlList = []

    if isinstance(news_url, str):
        urlList = [news_url]
    elif isinstance(news_url, list):
        urlList = news_url
    else:
        return []

    infoResultList = []

    for idx, nowUrl in zip(tqdm(urlList, desc=None), urlList):
        #print(idx)
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        resp = requests.get(nowUrl, headers=headers, verify=False)

        content_type = resp.headers['content-type']

        if not 'charset' in content_type:
            resp.encoding = resp.apparent_encoding

        print ("\n", nowUrl, resp.encoding)

        soup = BeautifulSoup(resp.text, 'lxml')

        infoResultList.append({
            "날짜":     getData(soup, metaData['date']), 
            "언론사":   getData(soup, metaData['publisher']), 
            "작성자":   getData(soup, metaData['author']), 
            "제목":     getData(soup, metaData['title']), 
            "요약":     getData(soup, metaData['summary']),
            "링크":     nowUrl
        })

    return infoResultList
    

def getData(soup, metaList):
    resultData = []

    for nowMeta in metaList:
        result = soup.find_all('meta', {nowMeta['type']: re.compile(nowMeta['value'])})

        for nowResult in result:
            if (nowResult.has_attr('content')):
                resultData.append(nowResult['content'])

    if len(resultData) == 0:
        return ""
            
    return min(resultData, key=len)
