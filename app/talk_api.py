# -*- coding: utf-8 -*-
# filename: talk_api.py

import json
import requests
import sys

sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret.nj_token import tuling_api_key

s = requests.session()

def talk(content, userid):
    url = 'http://www.tuling123.com/openapi/api'
    da = {"key": tuling_api_key, "info": content, "userid": userid}
    data = json.dumps(da)
    r = s.post(url, data=data)
    j = eval(r.text)
    code = j['code']
    print code
    if code == 100000:
        recontent = j['text']
    elif code == 200000:
        recontent = j['text'] + j['url']
    elif code == 302000:
        recontent = j['text'] + j['list'][0]['info'] + j['list'][0]['detailurl']
    elif code == 308000:
        recontent = j['text'] + j['list'][0]['info'] + j['list'][0]['detailurl']
    else:
        recontent = '这货还没学会怎么回复这句话'
    print recontent
    return recontent
