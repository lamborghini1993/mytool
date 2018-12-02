# -*- coding:utf-8 -*-
"""
@Author: lamborghini
@Date: 2018-04-02 20:28:07
@Desc:
"""

import os
import asyncio
import aiohttp
import time

from pubcode import misc


class CPubCrawler(object):
    m_Flag = ""
    m_MaxNum = 2000
    m_Encoding = "utf-8"
    m_DebugPrint = False
    m_MyHeader = {}
    m_Url = ""

    m_WrongChar = r"<>/|:\"*?"
    m_ConfigDir = "Config"
    m_DownDir = "Downloads"
    m_Headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gb2312,utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "Keep-alive"
    }

    def __init__(self):
        self.m_WaitingUrl = {}  # 等待爬虫的全部网页信息
        self.m_ReadyUrl = {}    # 准备爬虫的网页信息（根据优先级来，选取前m_MaxNum个需要爬取的网页）
        self.m_DoingUrl = {}    # 正在爬中的网页信息
        self.m_FailUrl = {}     # 爬取是吧的网页信息
        self.m_DoneInfo = {}    # 爬虫完毕之后保存的信息
        self.m_Loop = asyncio.get_event_loop()
        self.m_Headers.update(self.m_MyHeader)
        self._Init()
        self._Load()
        self._CustomInit()

    def _Init(self):
        self.m_DownPath = os.path.join(os.getcwd(), self.m_DownDir, self.m_Flag)
        self.m_ConfigPath = os.path.join(os.getcwd(), self.m_ConfigDir, self.m_Flag)
        for sDirPath in (self.m_DownPath, self.m_ConfigPath):
            if not os.path.exists(sDirPath):
                os.makedirs(sDirPath)

        self.m_WaitingConfigPath = os.path.join(self.m_ConfigPath, "Waiting.json")
        self.m_ReadyConfigPath = os.path.join(self.m_ConfigPath, "Ready.json")
        self.m_DoingConfigPath = os.path.join(self.m_ConfigPath, "Doing.json")
        self.m_DoneInfoConfigPath = os.path.join(self.m_ConfigPath, "DoneInfo.json")
        self.m_FailConfigPath = os.path.join(self.m_ConfigPath, "Fail.json")

        self.m_ErrorPath = os.path.join(self.m_ConfigPath, "error")
        self.m_LogPath = os.path.join(self.m_ConfigPath, "log")

    def _CustomInit(self):
        """自定义初始化网页信息"""
        pass

    def _Load(self):
        self.m_WaitingUrl = misc.JsonLoad(self.m_WaitingConfigPath, {})
        self.m_ReadyUrl = misc.JsonLoad(self.m_ReadyConfigPath, {})
        self.m_DoingUrl = misc.JsonLoad(self.m_DoingConfigPath, {})
        self.m_DoneInfo = misc.JsonLoad(self.m_DoneInfoConfigPath, {})
        self.m_FailUrl = misc.JsonLoad(self.m_FailConfigPath, {})

        self.DebugPrint("_Load")

        self.m_WaitingUrl.update(self.m_ReadyUrl)
        self.m_WaitingUrl.update(self.m_DoingUrl)
        self.m_ReadyUrl.clear()
        self.m_DoingUrl.clear()

    def _Save(self):
        self.DebugPrint("_Save")
        self._SaveOrDel(self.m_WaitingUrl, self.m_WaitingConfigPath)
        self._SaveOrDel(self.m_ReadyUrl, self.m_ReadyConfigPath)
        self._SaveOrDel(self.m_DoingUrl, self.m_DoingConfigPath)
        self._SaveOrDel(self.m_FailUrl, self.m_FailConfigPath)
        misc.JsonDump(self.m_DoneInfo, self.m_DoneInfoConfigPath)

    def _SaveOrDel(self, dInfo, sPath):
        """如果需要保存的信息为空，那么就删除文件"""
        if dInfo:
            misc.JsonDump(dInfo, sPath)
            return
        if os.path.exists(sPath):
            os.remove(sPath)

    def _Restart(self):
        time.sleep(1)
        self.DebugPrint("_Restart")
        self._Save()
        self._Load()
        self.Start()

    def Start(self):
        self.DebugPrint("Start_Begin")
        try:
            self.m_Loop.run_until_complete(self.Run())
            self.m_Loop.close()
        except OSError as e:
            info = misc.PythonError(str(e))
            misc.Write2File(self.m_ErrorPath, info, "a+")
            self._Restart()
            return
        except Exception as e:
            info = misc.PythonError(str(e))
            misc.Write2File(self.m_ErrorPath, info, "a+")

        self._Save()
        self.DebugPrint("Start_End")

    def _Replace(self, sMsg, default="_"):
        for char in self.m_WrongChar:
            if sMsg.find(char) == -1:
                continue
            sMsg = sMsg.replace(char, default)
        return sMsg

    def DebugPrint(self, msg):
        if self.m_DebugPrint:
            print(msg, "wait:%s read:%s doing:%s done:%s fail:%s" % (len(self.m_WaitingUrl), len(self.m_ReadyUrl), len(self.m_DoingUrl), len(self.m_DoneInfo), len(self.m_FailUrl)))

    def NewCrawel(self):
        self.m_WaitingUrl.update(self.m_DoingUrl)
        self.m_DoingUrl.clear()

        tInfo = []
        for url, dInfo in self.m_WaitingUrl.items():
            iType = dInfo.get("priority", 0)
            iTime = dInfo.get("time", misc.GetSecond())
            tInfo.append((url, iType, iTime))
        tInfo = sorted(tInfo, key=lambda x: x[2])   # 优先级高的在前面
        tInfo = sorted(tInfo, key=lambda x: x[1], reverse=True)  # 时间早的在前面

        while (len(self.m_ReadyUrl)) < self.m_MaxNum and tInfo:
            url, *args = tInfo.pop(0)
            self.m_ReadyUrl[url] = self.m_WaitingUrl.pop(url)
        return True

    async def Run(self):
        async with aiohttp.ClientSession() as self.m_Session:
            while self.NewCrawel() and (len(self.m_WaitingUrl) + len(self.m_ReadyUrl)):
                self.DebugPrint("Run")
                if not self.m_ReadyUrl:
                    await asyncio.sleep(0.1)
                    continue

                tasks = []
                for url, dInfo in self.m_ReadyUrl.items():
                    oTask = self.m_Loop.create_task(self.Crawl(url, dInfo))
                    tasks.append(oTask)
                self.m_DoingUrl.update(self.m_ReadyUrl)
                self.m_ReadyUrl.clear()

                finished, unfinished = await asyncio.wait(tasks)
                if unfinished:
                    print("="*20, unfinished)
                htmls = [f.result() for f in finished]
                for url, dInfo, html in htmls:
                    await self.Parse(url, dInfo, html)

    async def Crawl(self, url, dInfo):
        r = await self.m_Session.get(url, headers=self.m_Headers)
        html = await r.text(encoding=self.m_Encoding)
        return url, dInfo, html

    async def Parse(self, url, dInfo, html):
        """爬取成功之后从Doing和Fail中删除"""
        # doing my Parse
        await self.MyParse(url, dInfo, html)
        if url in self.m_DoingUrl:
            del self.m_DoingUrl[url]
        if url in self.m_FailUrl:
            del self.m_FailUrl[url]

    async def MyParse(self, url, dInfo, html):
        pass
