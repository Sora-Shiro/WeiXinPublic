# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web

import reply
import receive

import sys

sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret import nj_token

a_name = "a"
b_name = "b"
c_name = "c"
d_name = "d"
e_name = "e"

nick_names = ["1", "2", "3", "4", "5"]

vote_names = [a_name, b_name, c_name, d_name, e_name]

nick_to_real_map = dict(zip(nick_names, vote_names))

name_vote_map = {
    a_name: 0,
    b_name: 0,
    c_name: 0,
    d_name: 0,
    e_name: 0
}

fans_number_set = {}
admin_number_set = {"tomatoes11", "farseerleo"}



class Handle(object):
    def POST(self):
        global a_name, b_name, c_name, d_name, e_name
        global vote_names, name_vote_map, fans_number_set
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                show_str = ""
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if (recMsg.Content == 'Leo'):
                    show_str = u"Leo 超帅"
                elif recMsg.Content in nick_names:
                    # 检测是否为管理员
                    if toUser in admin_number_set:
                        nick_name = recMsg.Content
                        real_name = nick_to_real_map[nick_name]
                        name_vote_map[real_name] += 1
                    else:
                        # 检测该id是否已经投票
                        if toUser in fans_number_set:
                            show_str = u"您已经投过票，谢谢参与！"
                        else:
                            fans_number_set.add(toUser)
                            nick_name = recMsg.Content
                            real_name = nick_to_real_map[nick_name]
                            name_vote_map[real_name] += 1
                    # 展示结果
                    for nick_name in nick_names:
                        real_name = nick_to_real_map[nick_name]
                        show_str += u"%s号，%s得票数为：%d" % (nick_name, real_name, name_vote_map[real_name])
                        if vote_names[-1] != real_name:
                            show_str += "\n"
                else:
                    # 展示结果
                    for nick_name in nick_names:
                        real_name = nick_to_real_map[nick_name]
                        show_str += u"%s号，%s得票数为：%d" % (nick_name, real_name, name_vote_map[real_name])
                        if vote_names[-1] != real_name:
                            show_str += "\n"
                # 格式化最终字符串
                content = show_str.encode('utf-8')
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            else:
                print "暂且不处理"
                return "success"
        except Exception, Argment:
            return Argment
