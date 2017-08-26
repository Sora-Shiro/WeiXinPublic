# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

import reply
import receive

import sys

sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret import nj_token

a = 0
b = 0
c = 0
d = 0
e = 0


class Handle(object):
    def POST(self):
        global a, b, c, d, e
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
                    show_str = "a的当前得票数:%d" % a + "\nb的当前得票数:%d" % b +\
                               "\nc的当前得票数:%d" % c + "\nd的当前得票数:%d" % d + "\ne的当前得票数:%d" % e
                    show_str = show_str.decode('UTF-8').encode('GBK')
                    content = show_str
                elif (recMsg.Content == '2'):
                    b += 1
                    content = (str(u"a当前得票数:" + a)).encode('utf-8')
                elif (recMsg.Content == '3'):
                    c += 1
                    content = (u"a当前得票数:" + str(a).encode('utf-8')).encode('utf-8')
                elif (recMsg.Content == '4'):
                    d += 1
                    show_str = u"a的当前得票数:%d" % a + u"b的当前得票数:%d" % b
                    show_str = show_str.encode('utf-8')
                    content = show_str
                elif (recMsg.Content == '5'):
                    e += 1
                    content = (u"a当前得票数:" + str(a)).encode('utf-8')
                else:
                    show_str = u"%s" % ("a当前得票数:" + str(a))
                    content = show_str.encode('utf-8')
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment
