# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

import reply
import receive

import sys

sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret import nj_token


class Handle(object):
    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if(recMsg.Conten == 'Leo'):
                    content = u"Leo 超帅".encode('GBK')
                content = "Who are you"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment
