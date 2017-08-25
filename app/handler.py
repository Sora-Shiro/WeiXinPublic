# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

'''
CentOS need to add below code
```
import sys
sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
```
'''

from secret import nj_token


class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = nj_token.token  # 请按照公众平台官网\基本配置中信息填写

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            # print "handle/GET func: hashcode, signature: ", hashcode, signature
            print "Here is something from fans:\n"
            print data.Content
            print "\n"
            print data.FromUserName
            if hashcode == signature:
                return echostr
            else:
                print data.Content
                return ""
        except Exception, Argument:
            return Argument
