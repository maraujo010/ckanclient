from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
import json
import re
import asyncio
import aiohttp

ApiUrl          = "http://demo.ckan.org/api/3/action/"
DatasetListSrc  = "package_list"
DatasetSrc      = "package_show"

class CkanClient:
    'ckan asynchronous api client'

    def __init__(self):
        self.Datasets  = []
        self.NIntRsrc  = 0
        self.NExtRsrc  = 0
        self.connector = aiohttp.TCPConnector()
        self.semaphor  = asyncio.Semaphore(5)

    def ProcessData(self):
        try:
            req  = Request(ApiUrl + DatasetListSrc)
            res  = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
        else:
            data     = res.read()
            enc      = res.info().get_content_charset('utf-8')
            jsonData = json.loads(data.decode(enc))

            if jsonData["success"]:
                print("Fetching Datasets...")

                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait([self.fetch( ApiUrl + DatasetSrc + '?' + urlencode({ "id" :DatasetID })) for DatasetID in jsonData["result"]]))
                loop.close()

            else:
                print (jsonData["error"])

    # fetch Dataset Info
    @asyncio.coroutine
    def fetch(self, url):
        try:
            with (yield from self.semaphor):
                response = yield from aiohttp.request('get', url, connector=self.connector)
                print(url)
        except URLError as e:
            if hasattr(e, 'reason'):
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('Error code: ', e.code)
        else:
            enc      = (yield from response.read()).decode('utf-8')
            jsonData = json.loads(enc)

            if jsonData["success"]:
                self.Datasets.append(jsonData["result"])

                for Rsrc in jsonData["result"]["resources"]:
                    pattern = r"http://demo.ckan.org/dataset/(.*)/resource/(.*)/download"

                    if re.search(pattern, Rsrc["url"]):
                        self.NIntRsrc += 1
                    else:
                        self.NExtRsrc += 1
