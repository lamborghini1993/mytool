# -*- coding: utf-8 -*-
"""
@Author: lamborghini1993
@Date: 2017-11-02 16:03:23
@Last Modified by:   lamborghini1993
@Last Modified time: 2017-11-02 16:03:23
@Desc:
    爬虫
"""


import urllib.request
import bs4
from mytool import pubdefines


class CWebCrawler(object):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) \
            Gecko/20100101 Firefox/57.0"
    }
    logname = "webcrawler"

    def log(self, msg):
        pubdefines.write_to_file(self.logname, msg)

    def get_bs4_by_url(self, url, coding="utf-8", trynum=10, timeout=10):
        for num in range(trynum):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(req, timeout=timeout)
                bs4obj = bs4.BeautifulSoup(
                    response, "html.parser", from_encoding=coding)
                return bs4obj
            except:
                pass
        self.log("失败{}次 {}".format(trynum, url))
        return None

    def get_data_by_url(self, url, coding="utf-8", trynum=10, timeout=10):
        for num in range(trynum):
            try:
                req = urllib.request.Request(url, headers=self.headers)
                response = urllib.request.urlopen(req, timeout=timeout)
                data = response.read()
                return data
            except:
                pass
        self.log("失败{}次 {}".format(trynum, url))
        return None


if "WEB_CRAWLER_OBJ" not in globals():
    WEB_CRAWLER_OBJ = CWebCrawler()
