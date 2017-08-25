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
    global a, b, c, d, e
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if (recMsg.Content == 'Leo'):
                    content = u"Leo 超帅".encode('utf-8')
                elif (recMsg.Content == '1'):
                    a += 1
                    content = ("a当前得票数:" + a + "b当前得票数:" + b + "c当前得票数:" + c + "d当前得票数:" + d + "e当前得票数:" + e).encode(
                        'utf-8')
                elif (recMsg.Content == '2'):
                    b += 1
                    content = (u"a当前得票数:" + a + u"b当前得票数:" + b + u"c当前得票数:" + c + u"d当前得票数:" + d + u"e当前得票数:" + e).encode(
                        'utf-8')
                elif (recMsg.Content == '3'):
                    c += 1
                    content = (u"a当前得票数:" + a + u"b当前得票数:" + b + u"c当前得票数:" + c + u"d当前得票数:" + d + u"e当前得票数:" + e).encode(
                        'utf-8')
                elif (recMsg.Content == '4'):
                    d += 1
                    content = (u"a当前得票数:" + a + u"b当前得票数:" + b + u"c当前得票数:" + c + u"d当前得票数:" + d + u"e当前得票数:" + e).encode(
                        'utf-8')
                elif (recMsg.Content == '5'):
                    e += 1
                    content = ("a当前得票数:" + a + "b当前得票数:" + b + "c当前得票数:" + c + "d当前得票数:" + d + "e当前得票数:" + e).encode(
                        'utf-8')
                else:
                    content = ("a当前得票数:" + a + "b当前得票数:" + b + "c当前得票数:" + c + "d当前得票数:" + d + "e当前得票数:" + e).encode(
                        'utf-8')
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment
