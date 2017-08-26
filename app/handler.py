# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

import reply
import receive

import sys

sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret import nj_token

a_vote = 0
b_vote = 0
c_vote = 0
d_vote = 0
e_vote = 0

a_name = "a"
b_name = "b"
c_name = "c"
d_name = "d"
e_name = "e"

vote_name_list = [a_name, b_name, c_name, d_name, e_name]

vote_map = {
    a_name: a_vote,
    b_name: b_vote,
    c_name: c_vote,
    d_name: d_vote,
    e_name: e_vote
}


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
                    show_str = ""
                    for name in vote_name_list :
                        show_str += u"%s的当前得票数%d" % (name, vote_map[name])
                        if vote_name_list[-1] != name:
                            show_str += "\n"
                    content = show_str.encode('utf-8')
                elif (recMsg.Content == '2'):
                    b += 1
                    show_str = ""
                    for name in vote_name_list:
                        show_str += u"%s的当前得票数%d" % (name, vote_map[name])
                        if vote_name_list[-1] != name:
                            show_str += "\n"
                    content = show_str.encode('utf-8')
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
                    show_str = u"%s" % (u"a当前得票数:" + str(a))
                    content = show_str.encode('utf-8')
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment
