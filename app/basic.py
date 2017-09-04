# -*- coding: utf-8 -*-
# filename: basic.py

"""
再次重复说明，下面代码只是为了简单说明接口获取方式。
实际中并不推荐，尤其是业务繁重的公众号，更需要中控服务器，统一的获取accessToken。
"""

import urllib
import time
import json

import sys
sys.path.append('/root/WeiXinPublic/WeiXinPublic')
from secret.nj_token import app_id, app_secret


class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):
        appId = app_id
        appSecret = app_secret

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())

        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']

    def get_access_token(self):
        if self.__leftTime < 10:
            self.__real_get_access_token()
        return self.__accessToken

    def run(self):
        while (True):
            if self.__leftTime > 10:
                time.sleep(2)
                self.__leftTime -= 2
            else:
                self.__real_get_access_token()
