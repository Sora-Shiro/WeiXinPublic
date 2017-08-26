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

real_names = [a_name, b_name, c_name, d_name, e_name]

nick_to_real_map = dict(zip(nick_names, real_names))

real_to_vote_map = {
    a_name: 0,
    b_name: 0,
    c_name: 0,
    d_name: 0,
    e_name: 0
}

fans_number_set = set()
admin_number_set = set(["tomatoes11", "farseerleo",
                        "o_hn0s0hhaGPwHfZ9mWo8RtnWA2A",
                        "o_hn0szZLZ3nhY7m-9b9mSaqWRE0"])


class Handle(object):
    def POST(self):
        global real_names, real_to_vote_map, fans_number_set, nick_to_real_map, admin_number_set
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                show_str = u"debug"
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if (recMsg.Content == 'Leo'):
                    show_str = u"Leo 超帅"
                '''
                # revote enable 指令可以让发送者成为管理员
                if recMsg.Content == "revote enable":
                    admin_number_set.add(toUser)
                    show_str = u"Revote Enable"
                # revote disable 指令可以让发送者的管理员身份失效
                elif recMsg.Content == "revote disable":
                    if toUser in admin_number_set:
                        admin_number_set.remove(toUser)
                        show_str = u"Rovote Disable"
                '''
                # 修改选手名字：alter [nickname] [realname]
                if recMsg.Content.startswith("alter"):
                    process_str = recMsg.Content.split()
                    # 获取要更改的 nickname ，将其对应的 realname 改变
                    nick = process_str[1]

                    real = process_str[2]
                    print real
                    # real = u"%s" % (process_str[2].encode('utf-8'))
                    # print real
                    # real = u"%s" % (process_str[2].decode('gbk'))
                    # print real
                    # real = u"%s" % (process_str[2].decode('utf-8'))
                    # print real

                    real_before = nick_to_real_map[nick]
                    # 更新 数据
                    real_name_list_index = real_names.index(real_before)
                    real_names[real_name_list_index] = real
                    nick_to_real_map = dict(zip(nick_names, real_names))
                    vote = real_to_vote_map[real_before]
                    del real_to_vote_map[real_before]
                    real_to_vote_map[real] = vote
                # 增加选手：add [nickname] [realname]
                elif recMsg.Content.startswith("add"):
                    process_str = recMsg.Content.split()
                    # 获取要添加的 nickname 和对应的 realname
                    nick = process_str[1]
                    real = u"%s" % process_str[2]
                    # 更新 数据
                    nick_names.append(nick)
                    real_names.append(real)
                    nick_to_real_map = dict(zip(nick_names, real_names))
                    vote = 0
                    real_to_vote_map[real] = vote
                # 修改票数：votec [nickname] [votes]
                elif recMsg.Content.startswith("votec"):
                    process_str = recMsg.Content.split()
                    # 获取要修改票数的 nickname 和对应的 votes
                    nick = process_str[1]
                    votes = process_str[2]
                    votes = int(votes)
                    # 更新 数据
                    real = nick_to_real_map[nick]
                    real_to_vote_map[real] = votes
                # 投票检验
                elif recMsg.Content in nick_names:
                    # 检测是否为管理员
                    if toUser in admin_number_set:
                        nick_name = recMsg.Content
                        real_name = nick_to_real_map[nick_name]
                        real_to_vote_map[real_name] += 1
                    else:
                        # 检测该id是否已经投票
                        if toUser in fans_number_set:
                            show_str = u"您已经投过票，谢谢参与！\n"
                        else:
                            fans_number_set.add(toUser)
                            nick_name = recMsg.Content
                            real_name = nick_to_real_map[nick_name]
                            real_to_vote_map[real_name] += 1
                    # 展示结果
                    for nick_name in nick_names:
                        real_name = nick_to_real_map[nick_name]
                        show_str += u"%s号，%s得票数为：%d" % (nick_name, real_name, real_to_vote_map[real_name])
                        if real_names[-1] != real_name:
                            show_str += "\n"
                else:
                    # 展示结果
                    for nick_name in nick_names:
                        real_name = nick_to_real_map[nick_name]
                        print real_name
                        print "ahh"
                        print real_to_vote_map[real_name]
                        print "pre"
                        show_str += nick_name + " : " + real_name + " : " + real_to_vote_map[real_name]
                        if real_names[-1] != real_name:
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


def save_votes():
    save_votes_in_txt()
    return ""


def save_votes_in_txt():
    return ""
