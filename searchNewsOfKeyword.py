from bs4 import BeautifulSoup
import requests
import base64
import binascii

def findNewsOfKeyword(keyword):
    url = "https://news.google.com/search?q={0}&hl=ko&gl=KR&ceid=KR:ko".format(keyword)

    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')

    news = soup.select('[id="yDmH0d"] > c-wiz > div > div > div > div > main > c-wiz > div > div > a')

    newsLinks = []

    for idx, newsLink in enumerate(news):
        href = base64ToUrl(newsLink.get('href'))

        newsLinks.append(href)

    return newsLinks

def base64ToUrl(h):
    hrefBase64 = h[11: -25].replace('_', '/').replace('-', '+')

    if hrefBase64.find('uo=') != -1:
        hrefBase64 = hrefBase64[hrefBase64.find('uo=') + 3:]

    hrefBase64 += '=' * (4 - len(hrefBase64) % 4)
    hrefHex = base64.b64decode(hrefBase64).hex()
    hrefHexFiltering = ""

    for i in range(len(hrefHex)):
        if i&1 == 0:
            nowHex = hrefHex[i:i+2]

            if nowHex[0] >= '2' and nowHex[0] <= '7':
                hrefHexFiltering += nowHex

    hrefBinary = binascii.unhexlify(hrefHexFiltering)

    href = hrefBinary.decode('ascii')

    if href.find('http', 4) != -1:
        href = href[href.find('http', 4):]
    else:
        while href[0] != 'h':
            href = href[1:]
    
    return href