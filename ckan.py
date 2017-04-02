from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode
import json
import re

ApiUrl          = "http://demo.ckan.org/api/3/action/"
DatasetListSrc  = "package_list"
DatasetSrc      = "package_show"

class CkanClient:
    'ckan api client'

    def __init__(self):
        self.Datasets = []
        self.NIntRsrc = 0
        self.NExtRsrc = 0

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

                for DatasetID in jsonData["result"]:
                    try:
                        qStr = urlencode({ "id" :DatasetID })
                        req  = Request(ApiUrl + DatasetSrc + '?' + qStr)
                        res  = urlopen(req)
                    except URLError as e:
                        if hasattr(e, 'reason'):
                            print('Reason: ', e.reason)
                        elif hasattr(e, 'code'):
                            print('Error code: ', e.code)
                    else:
                        print(DatasetID)
                        data     = res.read()
                        enc      = res.info().get_content_charset('utf-8')
                        jsonData = json.loads(data.decode(enc))

                        if jsonData["success"]:
                            self.Datasets.append(jsonData["result"])

                            for Rsrc in jsonData["result"]["resources"]:
                                pattern = r"http://demo.ckan.org/dataset/(.*)/resource/(.*)/download"

                                if re.search(pattern, Rsrc["url"]):
                                    if self.IsRsrcAvailable(Rsrc["url"]):
                                        self.NIntRsrc += 1
                                else:
                                    self.NExtRsrc += 1
                        else:
                            print(jsonData["error"]["message"])

    # check if the resource is available
    def IsRsrcAvailable(self, RsrcUrl):
        try:
            status = urlopen(RsrcUrl).getcode()
        except HTTPError as e:
            status = e.code

        return status in (200, 301, 302)
