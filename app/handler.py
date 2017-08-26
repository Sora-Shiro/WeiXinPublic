# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import codecs

import reply
import receive

import sys

sys.path.append('/root/PycharmProjects/GitWeiXinPublic/WeiXinPublic')
from secret import nj_token

# reload(sys)
# sys.setdefaultencoding('utf8')

nick_names = ["1", "2", "3", "4", "5"]

real_names = ["a", "b", "c", "d", "e"]

nick_to_real_map = dict(zip(nick_names, real_names))

real_to_vote_map = dict(zip(real_names, [0] * len(real_names)))

fans_number_set = set()
admins = ["tomatoes11", "farseerleo",
          "o_hn0s0hhaGPwHfZ9mWo8RtnWA2A",
          "o_hn0szZLZ3nhY7m-9b9mSaqWRE0"]
admin_number_set = set(admins)


class Handle(object):
    def POST(self):
        global real_names, real_to_vote_map, fans_number_set, nick_to_real_map, admin_number_set
        try:
            read_votes_in_txt()
            webData = web.data()
            print "Handle Post webdata is ", webData  # 后台打日志
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg) and recMsg.MsgType == 'text':
                show_str = u""
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
                # 检测是否为管理员
                if toUser in admin_number_set:
                    # 修改选手名字：alter [nickname] [realname]
                    if recMsg.Content.startswith("alter"):
                        show_str = u"alter"
                        process_str = recMsg.Content.split()
                        # 获取要更改的 nickname ，将其对应的 realname 改变
                        nick = process_str[1]
                        real = process_str[2]
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
                        show_str = u"add"
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
                    # 删除选手：del [nickname]
                    elif recMsg.Content.startswith("del"):
                        show_str = u"del"
                        process_str = recMsg.Content.split()
                        # 获取要删除的 nickname
                        nick = process_str[1]
                        if nick in process_str:
                            real = nick_to_real_map[nick]
                            nick_names.remove(nick)
                            real_names.remove(real)
                            del nick_to_real_map[nick]
                            del real_to_vote_map[real]
                    # 修改票数：votec [nickname] [votes]
                    elif recMsg.Content.startswith("votec"):
                        show_str = u"votec"
                        process_str = recMsg.Content.split()
                        # 获取要修改票数的 nickname 和对应的 votes
                        nick = process_str[1]
                        votes = process_str[2]
                        votes = int(votes)
                        # 更新 数据
                        real = nick_to_real_map[nick]
                        real_to_vote_map[real] = votes
                    # 复位票数和已投票粉丝：
                    elif recMsg.Content.startswith("reset"):
                        init_all_data()
                    # 投票检验
                    else:
                        nick_name = recMsg.Content
                        if nick_name in nick_names:
                            real_name = nick_to_real_map[nick_name]
                            real_to_vote_map[real_name] += 1
                        else:
                            show_str = u"没有这个号数的选手哦(⊙□⊙)"
                else:
                    # 检测该非管理员人员是否已经投票
                    if toUser in fans_number_set:
                        show_str = u"您已经投过票，谢谢参与！(*´▽｀* )\n"
                    # 投票检验
                    else:
                        fans_number_set.add(toUser)
                        nick_name = recMsg.Content
                        if nick_name in nick_names:
                            real_name = nick_to_real_map[nick_name]
                            real_to_vote_map[real_name] += 1
                        else:
                            show_str = u"没有这个号数的选手哦(⊙□⊙)"
                # 展示结果
                for nick_name in nick_names:
                    real_name = nick_to_real_map[nick_name]
                    show_str += u"%s号，%s得票数为：%d" % (nick_name, real_name, real_to_vote_map[real_name])
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


def init_all_data(nick=None, real=None, ntr_map=None, rtv_map=None):

    if nick is None:
        nick = ["1", "2", "3", "4", "5"]
    if real is None:
        real = ["a", "b", "c", "d", "e"]
    if ntr_map is None:
        ntr_map = dict(zip(nick_names, real_names))
    if rtv_map is None:
        rtv_map = dict(zip(real_names, [0] * len(real_names)))

    global nick_names, real_names, nick_to_real_map, real_to_vote_map, fans_number_set

    nick_names = nick

    real_names = real

    nick_to_real_map = ntr_map

    real_to_vote_map = rtv_map

    fans_number_set = set()


def save_votes():
    save_votes_in_txt()
    return ""


def save_votes_in_txt():
    return ""


def read_votes_in_txt():
    import codecs
    with codecs.open('/root/PycharmProjects/GitWeiXinPublic/votes.txt', 'r', 'utf-8') as f:
        for line in f.readlines():
            # 数据格式：[nickname] [realname] [votes]
            process_str = line.split()
            nick = process_str[0]
            real = process_str[1]
            votes = process_str[2]
            print nick
            print real
            print votes
    return ""
